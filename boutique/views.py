
from django.shortcuts import render, get_object_or_404, redirect
from paiements.models import Paiement
from produits.models import Produit, Categorie
from clients.models import Client
from clients.decorators import client_login_required
from ventes.models import Vente, LigneVente
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from livraisons.models import ZoneLivraison
from paiements.paydunya import verifier_paiement_paydunya
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# from paiements.cinetpay import initialiser_paiement_cinetpay
from paiements.paydunya import creer_facture_paydunya
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import requests
def client_associe_a_utilisateur(utilisateur):
    """Retrouve le profil Client à partir de l'e-mail, puis du téléphone."""
    email = (getattr(utilisateur, "email", "") or "").strip()
    telephone = (getattr(utilisateur, "telephone", "") or "").strip()

    if email:
        client = Client.objects.filter(email__iexact=email).first()
        if client:
            return client

    if telephone:
        return Client.objects.filter(telephone=telephone).first()

    return None


def accueil(request):
    produits = Produit.objects.filter(
        prix_vente__gt=0
    ).select_related(
        "categorie"
    ).order_by(
        "-date_creation"
    )
    categories = Categorie.objects.all().order_by("nom")
    return render(
        request,
        "boutique/accueil.html",
        {
            "produits": produits,
            "categories": categories,
        }
    )
def detail_produit(request, produit_id):
    produit = get_object_or_404(
        Produit,
        id=produit_id
    )
    return render(
        request,
        "boutique/detail_produit.html",
        {
            "produit": produit
        }
    )
def panier(request):
    panier_session = request.session.get("panier", {})
    print("PANIER DANS LA VUE :", panier_session)
    produits = []
    total = 0
    for produit_id, quantite in panier_session.items():
        produit = get_object_or_404(
            Produit,
            id=produit_id
        )
        sous_total = produit.prix_vente * quantite
        produits.append({
            "produit": produit,
            "quantite": quantite,
            "sous_total": sous_total,
        })
        total += sous_total
    return render(
        request,
        "boutique/panier.html",
        {
            "produits_panier": produits,
            "total": total,
        }
    )
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = request.session.get("panier", {})
    produit_id = str(produit_id)
    try:
        quantite = int(request.POST.get("quantite", 1))
    except (TypeError, ValueError):
        quantite = 1
    if quantite < 1:
        quantite = 1
    panier[produit_id] = panier.get(produit_id, 0) + quantite
    request.session["panier"] = panier
    request.session.modified = True
    print("PANIER APRES AJOUT :", request.session["panier"])
    return redirect("panier")
def augmenter_quantite(request, produit_id):
    panier = request.session.get(
        "panier",
        {}
    )
    produit_id = str(produit_id)
    if produit_id in panier:
        panier[produit_id] += 1
    request.session["panier"] = panier
    return redirect("panier")
def diminuer_quantite(request, produit_id):
    panier = request.session.get(
        "panier",
        {}
    )
    produit_id = str(produit_id)
    if produit_id in panier:
        panier[produit_id] -= 1
        if panier[produit_id] <= 0:
            del panier[produit_id]
    request.session["panier"] = panier
    return redirect("panier")
# =========================================================
# MODIFIER QUANTITE
# =========================================================
def modifier_quantite_panier(
    request,
    produit_id
):
    panier = request.session.get(
        "panier",
        {}
    )
    produit_id = str(produit_id)
    if produit_id not in panier:
        return redirect("panier")
    action = request.POST.get(
        "action"
    )
    if action == "plus":
        panier[produit_id] += 1
    elif action == "moins":
        panier[produit_id] -= 1
        if panier[produit_id] <= 0:
            del panier[produit_id]
    request.session["panier"] = panier
    request.session.modified = True
    return redirect("panier")
def supprimer_du_panier(request, produit_id):
    panier = request.session.get(
        "panier",
        {}
    )
    produit_id = str(produit_id)
    if produit_id in panier:
        del panier[produit_id]
    request.session["panier"] = panier
    return redirect("panier")
@client_login_required
def choisir_zone_livraison(request):
    zones = ZoneLivraison.objects.all().order_by("nom")
    panier_session = request.session.get("panier", {})
    if not panier_session:
        return redirect("panier")
    if request.method == "POST":
        zone_id = request.POST.get("zone_id")
        if not zone_id:
            messages.error(
                request,
                "Veuillez choisir une zone de livraison."
            )
            return redirect("choisir_zone_livraison")
        zone = get_object_or_404(
            ZoneLivraison,
            id=zone_id
        )
        # On conserve la zone dans la session
        request.session["zone_livraison_id"] = zone.id
        request.session.modified = True
        print("===================================")
        print("ZONE DE LIVRAISON")
        print("ZONE :", zone.nom)
        print("FRAIS :", zone.frais)
        print("===================================")
        return redirect("passer_commande")
    return render(
        request,
        "boutique/choisir_zone_livraison.html",
        {
            "zones": zones
        }
    )
@client_login_required
@transaction.atomic
def passer_commande(request):
    panier_session = request.session.get("panier", {})
    print("===================================")
    print("PASSER COMMANDE")
    print("UTILISATEUR :", request.user)
    print("EMAIL :", request.user.email)
    print("PANIER :", panier_session)
    print("===================================")
    if not panier_session:
        return redirect("panier")
    # ==============================
    # RÉCUPÉRER LE CLIENT
    # ==============================
    client = get_object_or_404(
    Client,
    id=request.session["client_id"]
)
    if not client:
        messages.error(
            request,
            "Aucun profil client ne correspond à votre compte. "
            "Vérifiez l'e-mail ou le téléphone de votre profil client."
        )
        return redirect("accueil")
    # ==============================
    # RÉCUPÉRER LA ZONE
    # ==============================
    zone_id = request.session.get(
        "zone_livraison_id"
    )
    if not zone_id:
        messages.warning(
            request,
            "Veuillez choisir votre zone de livraison."
        )
        return redirect(
            "choisir_zone_livraison"
        )
    zone = get_object_or_404(
        ZoneLivraison,
        id=zone_id
    )
    # ==============================
    # CRÉATION DE LA VENTE
    # ==============================
    vente = Vente.objects.create(
        client=client,
        type_vente="EN_LIGNE",
        statut="BROUILLON",
        montant_total=0,
        frais_livraison=zone.frais,
    )
    total_produits = 0
    # ==============================
    # CRÉATION DES LIGNES
    # ==============================
    for produit_id, quantite in panier_session.items():
        produit = get_object_or_404(
            Produit,
            id=produit_id
        )
        LigneVente.objects.create(
            vente=vente,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix_vente,
        )
        total_produits += (
            produit.prix_vente * quantite
        )
    # ==============================
    # TOTAL AVEC LIVRAISON
    # ==============================
    vente.montant_total = (
        total_produits + zone.frais
    )
    vente.save(
        update_fields=[
            "montant_total",
            "frais_livraison"
        ]
    )
    print("===================================")
    print("VENTE CREEE :", vente.id)
    print("ZONE :", zone.nom)
    print("PRODUITS :", total_produits)
    print("LIVRAISON :", zone.frais)
    print("TOTAL :", vente.montant_total)
    print("===================================")
    # ==============================
    # CRÉER LA LIVRAISON
    # ==============================
    # Pour l'instant la livraison est préparée.
    # Nous conserverons la zone sélectionnée.
    from livraisons.models import Livraison
    Livraison.objects.create(
        vente=vente,
        adresse_livraison=zone.nom,
        zone=zone,
        statut="EN_PREPARATION",
    )
    # ==============================
    # VIDER LE PANIER
    # ==============================
    request.session["panier"] = {}
    # La zone n'est plus nécessaire
    request.session.pop(
        "zone_livraison_id",
        None
    )
    request.session.modified = True
    # ==============================
    # PAIEMENT
    # ==============================
    print(
        "REDIRECTION VERS :",
        f"/commande/{vente.id}/payer/"
    )
    return redirect(
        "payer_commande",
        vente_id=vente.id
    )
@client_login_required
def mes_commandes(request):
    client = get_object_or_404(
    Client,
    id=request.session["client_id"]
)
    if not client:
        messages.error(
            request,
            "Aucun profil client n'est associé à votre compte. "
            "Vérifiez l'e-mail ou le téléphone de votre profil client."
        )
        return redirect("accueil")

    commandes = Vente.objects.filter(
        client=client,
        type_vente="EN_LIGNE"
    ).order_by("-date_vente")

    return render(
        request,
        "boutique/mes_commandes.html",
        {"client": client, "commandes": commandes}
    )

@client_login_required
def detail_commande(request, vente_id):
    client = get_object_or_404(
    Client,
    id=request.session["client_id"]
)
    if not client:
        messages.error(
            request,
            "Aucun profil client n'est associé à votre compte."
        )
        return redirect("accueil")

    commande = get_object_or_404(
        Vente,
        id=vente_id,
        client=client,
        type_vente="EN_LIGNE"
    )
    lignes = commande.lignes.select_related("produit")

    return render(
        request,
        "boutique/detail_commande.html",
        {
            "client": client,
            "commande": commande,
            "lignes": lignes,
        }
    )

@client_login_required
def payer_commande(request, vente_id):
    # ==============================
    # UTILISATEUR CONNECTÉ
    # ==============================
    client = get_object_or_404(
    Client,
    id=request.session["client_id"]
)
    if not client:
        messages.error(
            request,
            "Aucun profil client n'est associé à votre compte. "
            "Vérifiez l'e-mail ou le téléphone du profil client."
        )
        return redirect("accueil")
    # ==============================
    # RÉCUPÉRER LA COMMANDE
    # ==============================
    commande = get_object_or_404(
        Vente,
        id=vente_id,
        client=client,
        type_vente="EN_LIGNE"
    )
    print("================================")
    print("PAGE PAIEMENT")
    print("CLIENT :", client)
    print("VENTE :", commande.id)
    print("STATUT :", commande.statut)
    print("================================")
    # ==============================
    # LA COMMANDE DOIT ÊTRE BROUILLON
    # ==============================
    if commande.statut != "BROUILLON":
        messages.error(
            request,
            "Cette commande ne peut plus être payée."
        )
        return redirect(
            "detail_commande",
            vente_id=commande.id
        )
    # ==============================
    # AFFICHAGE DE LA PAGE
    # ==============================
    if request.method == "GET":
        return render(
            request,
            "boutique/payer_commande.html",
            {
                "client": client,
                "commande": commande
            }
        )
    # ==============================
    # TRAITEMENT DU POST
    # ==============================
    mode_paiement = request.POST.get("mode_paiement")
    modes_autorises = [
        "ESPECES",
        "ORANGE_MONEY",
        "MOOV_MONEY",
        "CARTE",
    ]
    if mode_paiement not in modes_autorises:
        messages.error(
            request,
            "Veuillez choisir un mode de paiement."
        )
        return redirect(
            "payer_commande",
            vente_id=commande.id
        )
    # ==============================
    # CRÉATION / RÉCUPÉRATION PAIEMENT
    # ==============================
    paiement, created = Paiement.objects.get_or_create(
        vente=commande,
        defaults={
            "montant": commande.montant_total,
            "mode_paiement": mode_paiement,
            "statut": "EN_ATTENTE",
        }
    )
    if not created:
        paiement.mode_paiement = mode_paiement
        paiement.montant = commande.montant_total
        paiement.statut = "EN_ATTENTE"
        paiement.save()
    # ==============================
    # PAIEMENT ESPÈCES
    # ==============================
    if mode_paiement == "ESPECES":
        try:
            paiement.effectuer()
            messages.success(
                request,
                "Paiement enregistré avec succès. "
                "La commande est confirmée."
            )
        except Exception as e:
            
            print("ERREUR PAYDUNYA :", e)

            messages.error(
                request,
                "Le service de paiement est momentanément inaccessible. "
                "Aucun paiement n'a été confirmé. Réessaie plus tard."
            )

            return redirect(
                "payer_commande",
                vente_id=commande.id
            )
    # ==============================
    # PAYDUNYA
    # ORANGE MONEY / MOOV MONEY / CARTE
    # ==============================
    if mode_paiement in [
        "ORANGE_MONEY",
        "MOOV_MONEY",
        "CARTE",
    ]:
        try:
            callback_url = request.build_absolute_uri(
                reverse("paydunya_ipn")
            )
            return_url = request.build_absolute_uri(
                reverse(
                    "paydunya_retour",
                    kwargs={
                        "vente_id": commande.id
                    }
                )
            )
            cancel_url = request.build_absolute_uri(
                reverse(
                    "paydunya_annulation",
                    kwargs={
                        "vente_id": commande.id
                    }
                )
            )
            resultat = creer_facture_paydunya(
                montant=commande.montant_total,
                description=(
                    f"Commande Syllaraga #{commande.id}"
                ),
                callback_url=callback_url,
                return_url=return_url,
                cancel_url=cancel_url,
                client_nom=(
                    f"{client.prenom} {client.nom}"
                ),
                client_email=client.email,
                client_telephone=client.telephone,
                commande=commande,
            )
            print("================================")
            print("REPONSE PAYDUNYA :", resultat)
            print("================================")
            response_code = resultat.get(
                "response_code"
            )
            token = resultat.get(
                "token"
            )
            payment_url = resultat.get("response_text")
            # PayDunya renvoie response_code == "00" en cas de succès.
            # response_text contient alors l'URL de paiement.
            if str(response_code) != "00":
                print("ECHEC CREATION FACTURE PAYDUNYA :", resultat)
                messages.error(
                    request,
                    "PayDunya n'a pas pu créer la facture. Veuillez réessayer."
                )
                return redirect("detail_commande", vente_id=commande.id)
            if not token or not payment_url:
                messages.error(
                    request,
                    "PayDunya n'a pas retourné le token ou le lien de paiement."
                )
                return redirect("detail_commande", vente_id=commande.id)
            # Le modèle utilise actuellement reference_cinetpay pour stocker le token PayDunya.
            paiement.reference_cinetpay = token
            paiement.statut = "EN_ATTENTE"
            paiement.save(update_fields=["reference_cinetpay", "statut"])
            print("TOKEN PAYDUNYA :", token)
            print("URL PAYDUNYA :", payment_url)
            return redirect(payment_url)
        except Exception as e:
            print(
                "ERREUR PAYDUNYA :",
                e
            )
            messages.error(
                request,
                f"Impossible d'initialiser PayDunya : {str(e)}"
            )
            return redirect(
                "detail_commande",
                vente_id=commande.id
            )
@csrf_exempt
def paydunya_ipn(request):
    if request.method != "POST":
        return JsonResponse({"status": "method_not_allowed"}, status=405)

    try:
        donnees_brutes = request.POST.get("data")
        if not donnees_brutes:
            return JsonResponse({"status": "missing_data"}, status=400)

        if isinstance(donnees_brutes, dict):
            data = donnees_brutes
        else:
            data = json.loads(donnees_brutes)

        if not isinstance(data, dict):
            return JsonResponse({"status": "invalid_data"}, status=400)

        hash_recu = data.get("hash")
        hash_attendu = hashlib.sha512(
            settings.PAYDUNYA_MASTER_KEY.encode()
        ).hexdigest()

        if not hash_recu or hash_recu != hash_attendu:
            return JsonResponse({"status": "invalid_hash"}, status=403)

        statut = str(data.get("status", "")).strip().lower()
        invoice = data.get("invoice") or {}
        token = invoice.get("token")

        if not token:
            return JsonResponse({"status": "missing_token"}, status=400)

        paiement = (
            Paiement.objects
            .filter(reference_cinetpay=token)
            .select_related("vente")
            .first()
        )
        if not paiement:
            return JsonResponse({"status": "payment_not_found"}, status=404)

        if statut == "completed":
            if paiement.statut != "PAYE":
                paiement.effectuer()
            return JsonResponse({"status": "completed"})

        if statut in ("cancelled", "canceled", "failed"):
            if paiement.statut != "PAYE":
                paiement.statut = "ECHEC"
                paiement.save(update_fields=["statut"])
            return JsonResponse({"status": statut})

        return JsonResponse({"status": "pending"})

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({"status": "invalid_data"}, status=400)
    except Exception as e:
        print("ERREUR IPN PAYDUNYA :", e)
        return JsonResponse({"status": "error"}, status=500)
@client_login_required
def paydunya_retour(request, vente_id):
    client = get_object_or_404(
    Client,
    id=request.session["client_id"]
)
    if not client:
        messages.error(request, "Aucun profil client n'est associé à votre compte.")
        return redirect("accueil")

    commande = get_object_or_404(
        Vente,
        id=vente_id,
        client=client,
        type_vente="EN_LIGNE"
    )
    token = (request.GET.get("token") or "").strip()
    if not token:
        messages.error(request, "Token PayDunya introuvable dans l'URL de retour.")
        return redirect("detail_commande", vente_id=commande.id)

    paiement = Paiement.objects.filter(vente=commande).first()
    if not paiement:
        messages.error(request, "Paiement introuvable pour cette commande.")
        return redirect("detail_commande", vente_id=commande.id)

    # Le token reçu doit correspondre à celui sauvegardé à la création de facture.
    if not paiement.reference_cinetpay or token != paiement.reference_cinetpay:
        messages.error(request, "Le token PayDunya ne correspond pas au paiement attendu.")
        return redirect("detail_commande", vente_id=commande.id)

    try:
        url = (
            "https://app.paydunya.com/"
            "sandbox-api/v1/checkout-invoice/confirm/"
            f"{token}"
        )
        headers = {
            "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
            "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
            "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        resultat = response.json()
        statut = str(resultat.get("status", "")).strip().lower()

        if statut == "completed":
            if paiement.statut != "PAYE":
                paiement.effectuer()
            messages.success(
                request,
                "Paiement confirmé avec succès. Votre commande est confirmée."
            )
        elif statut == "pending":
            messages.info(
                request,
                "Votre paiement est encore en attente de confirmation."
            )
        elif statut in ("cancelled", "canceled"):
            if paiement.statut != "PAYE":
                paiement.statut = "ECHEC"
                paiement.save(update_fields=["statut"])
            messages.warning(request, "Le paiement a été annulé.")
        elif statut == "failed":
            if paiement.statut != "PAYE":
                paiement.statut = "ECHEC"
                paiement.save(update_fields=["statut"])
            messages.error(request, "Le paiement a échoué.")
        else:
            messages.info(
                request,
                "Le statut du paiement n'a pas pu être déterminé. "
                "La notification PayDunya pourra confirmer le résultat."
            )

    except Exception as e:
        print("ERREUR VERIFICATION PAYDUNYA :", e)
        messages.error(
            request,
            "Impossible de vérifier le paiement pour le moment."
        )

    return redirect("detail_commande", vente_id=commande.id)

@client_login_required
def paydunya_annulation(request, vente_id):
    client = get_object_or_404(
        Client,
        id=request.session["client_id"]
    )
    if not client:
        messages.error(request, "Aucun profil client n'est associé à votre compte.")
        return redirect("accueil")

    commande = get_object_or_404(
        Vente,
        id=vente_id,
        client=client,
        type_vente="EN_LIGNE"
    )

    paiement = Paiement.objects.filter(vente=commande).first()
    if paiement and paiement.statut != "PAYE":
        paiement.statut = "ECHEC"
        paiement.save(update_fields=["statut"])

    messages.warning(request, "Le paiement a été annulé.")
    return redirect("detail_commande", vente_id=commande.id)

def detail_produit(request, produit_id):
    produit = get_object_or_404(
        Produit.objects.select_related("categorie"),
        id=produit_id
    )
    return render(
        request,
        "boutique/detail_produit.html",
        {
            "produit": produit,
        }
    )
# def paiement_cinetpay_notification(request):
#     return JsonResponse({
#         "status": "ok"
#     })
# def paiement_cinetpay_retour(request, vente_id):
#     commande = get_object_or_404(
#         Vente,
#         id=vente_id,
#         type_vente="EN_LIGNE"
#     )
#     messages.info(
#         request,
#         "Votre paiement est en cours de traitement."
#     )
#     return redirect(
#         "detail_commande",
#         vente_id=commande.id
#     )
