
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import VenteForm, LigneVenteForm
from django.contrib import messages
from produits.models import Produit
from .models import Vente, LigneVente
from django.contrib.auth.decorators import login_required
from utilisateurs.decorators import role_requis
@login_required
def ajouter_vente(request):

    if request.method == "POST":

        form = VenteForm(request.POST)

        if form.is_valid():

            vente = form.save()

            return redirect(
                "detail_vente",
                id=vente.id
            )

    else:

        form = VenteForm()


    return render(
        request,
        "ventes/ajouter.html",
        {
            "form": form
        }
    )
@login_required
def detail_vente(request, id):

    vente = get_object_or_404(
        Vente,
        id=id
    )

    lignes = vente.lignes.all()

    produits = Produit.objects.all().order_by("nom")

    return render(
        request,
        "ventes/detail.html",
        {
            "vente": vente,
            "lignes": lignes,
            "produits": produits
        }
    )
@login_required    
def ajouter_produit_direct(request, id):

    if request.method != "POST":
        return JsonResponse(
            {"success": False},
            status=405
        )

    vente = get_object_or_404(
        Vente,
        id=id
    )

    if vente.statut != "BROUILLON":
        return JsonResponse({
            "success": False,
            "message": "Cette vente ne peut plus être modifiée."
        })

    produit_id = request.POST.get("produit_id")
    quantite = request.POST.get("quantite", 1)

    try:

        produit = Produit.objects.get(
            id=produit_id
        )

        quantite = int(quantite)

        if quantite < 1:
            raise ValueError

    except (Produit.DoesNotExist, ValueError):

        return JsonResponse({
            "success": False,
            "message": "Produit ou quantité invalide."
        })

    ligne = LigneVente.objects.filter(
        vente=vente,
        produit=produit
    ).first()

    if ligne:

        ligne.quantite += quantite
        ligne.save()

    else:

        ligne = LigneVente.objects.create(
            vente=vente,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix_vente
        )

    vente.calculer_montant_total()

    return JsonResponse({
        "success": True,
        "produit": produit.nom,
        "prix": str(produit.prix_vente),
        "quantite": ligne.quantite,
        "total_ligne": str(
            ligne.quantite * ligne.prix_unitaire
        ),
        "montant_total": str(
            vente.montant_total
        ),
        "ligne_id": ligne.id
    })
@login_required        
def ajouter_ligne_vente(request, id):

    vente = get_object_or_404(
        Vente,
        id=id
    )

    if vente.statut == "CONFIRMEE":
        return redirect(
            "detail_vente",
            id=vente.id
        )

    produits = Produit.objects.all().order_by("nom")

    if request.method == "POST":

        produit_id = request.POST.get("produit")
        quantite = request.POST.get("quantite")

        if not produit_id:
            messages.error(
                request,
                "Veuillez sélectionner un produit."
            )

        elif not quantite:
            messages.error(
                request,
                "Veuillez saisir une quantité."
            )

        else:

            try:

                produit = Produit.objects.get(
                    id=produit_id
                )

                quantite = int(quantite)

                if quantite < 1:
                    raise ValueError

                LigneVente.objects.create(
                    vente=vente,
                    produit=produit,
                    quantite=quantite,
                    prix_unitaire=produit.prix_vente
                )

                vente.calculer_montant_total()

                return redirect(
                    "detail_vente",
                    id=vente.id
                )

            except Produit.DoesNotExist:

                messages.error(
                    request,
                    "Produit introuvable."
                )

            except ValueError:

                messages.error(
                    request,
                    "La quantité doit être un nombre supérieur à 0."
                )

    return render(
        request,
        "ventes/ajouter_ligne.html",
        {
            "vente": vente,
            "produits": produits
        }
    )
@login_required    
def confirmer_vente(request, id):

    vente = get_object_or_404(
        Vente,
        id=id
    )

    try:

        vente.confirmer()

        messages.success(
            request,
            "La vente a été confirmée avec succès."
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )


    return redirect(
    "detail_vente",
    id=vente.id

    )
@login_required         
def annuler_vente(request, id):

    vente = get_object_or_404(
        Vente,
        id=id
    )

    try:

        vente.annuler()

        messages.success(
            request,
            "La vente a été annulée avec succès."
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

    return redirect(
        "detail_vente",
        id=vente.id
    )
@role_requis(roles=['ADMINISTRATEUR', 'VENDEUR'])      
def liste_ventes(request):

    ventes = Vente.objects.select_related(
        "client"
    ).order_by(
        "-date_vente"
    )

    return render(
        request,
        "ventes/liste.html",
        {
            "ventes": ventes
        }
    )     