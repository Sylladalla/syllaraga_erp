from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Achat
from .forms import AchatForm, LigneAchatFormSet
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
def liste_achats(request):

    achats = Achat.objects.select_related(
        "fournisseur"
    ).all().order_by(
        "-date_achat"
    )

    return render(
        request,
        "achats/liste.html",
        {
            "achats": achats
        }
    )



def ajouter_achat(request):

    if request.method == "POST":

        form = AchatForm(request.POST)

        if form.is_valid():

            achat = form.save()

            formset = LigneAchatFormSet(
                request.POST,
                instance=achat
            )

            if formset.is_valid():

                formset.save()

                achat.calculer_montant_total()

                return redirect(
                    "liste_achats"
                )

    else:

        form = AchatForm()

        formset = LigneAchatFormSet()


    return render(
        request,
        "achats/ajouter.html",
        {
            "form": form,
            "formset": formset
        }
    )
def detail_achat(request, id):

    achat = get_object_or_404(
        Achat,
        id=id
    )


    return render(
        request,
        "achats/detail.html",
        {
            "achat": achat
        }
    )
def receptionner_achat(request, id):

    achat = get_object_or_404(
        Achat,
        id=id
    )

    if achat.statut != "RECEPTIONNE":

        achat.receptionner()

        messages.success(
            request,
            "L'achat a été réceptionné avec succès."
        )

    else:

        messages.warning(
            request,
            "Cet achat est déjà réceptionné."
        )

    return redirect(
        "detail_achat",
        id=achat.id
    )        



def envoyer_achat(request, id):
    if request.method != "POST":
        return redirect("detail_achat", id=id)

    achat = get_object_or_404(
        Achat.objects.select_related("fournisseur"),
        id=id
    )

    if achat.statut != "BROUILLON":
        messages.warning(
            request,
            "Seul un achat en brouillon peut être envoyé au fournisseur."
        )
        return redirect("detail_achat", id=achat.id)

    lignes = list(achat.lignes.select_related("produit").all())

    if not lignes:
        messages.error(
            request,
            "Ajoutez au moins un produit avant d'envoyer la commande."
        )
        return redirect("detail_achat", id=achat.id)

    fournisseur = achat.fournisseur

    if not fournisseur.email:
        messages.error(
            request,
            "Ce fournisseur n'a pas d'adresse e-mail. "
            "Ajoutez son adresse avant l'envoi."
        )
        return redirect("detail_achat", id=achat.id)

    # Calculer le total sans modifier le statut
    total = sum(
        (ligne.quantite * ligne.prix_unitaire for ligne in lignes),
        start=0
    )

    details = []
    for ligne in lignes:
        sous_total = ligne.quantite * ligne.prix_unitaire
        details.append(
            f"- {ligne.produit.nom} : "
            f"{ligne.quantite} x {ligne.prix_unitaire} FCFA "
            f"= {sous_total} FCFA"
        )

    sujet = f"Commande fournisseur Syllaraga n°{achat.id}"

    message_email = (
        f"Bonjour {fournisseur.nom},\n\n"
        f"Nous souhaitons vous transmettre la commande n°{achat.id}.\n\n"
        "Détail de la commande :\n"
        + "\n".join(details)
        + f"\n\nMontant total : {total} FCFA\n\n"
        "Merci de nous confirmer la disponibilité des produits "
        "et le délai de livraison.\n\n"
        "Cordialement,\n"
        "L'équipe Syllaraga"
    )

    try:
        nombre_envoye = send_mail(
            subject=sujet,
            message=message_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[fournisseur.email],
            fail_silently=False,
        )

        if nombre_envoye != 1:
            messages.error(
                request,
                "L'e-mail n'a pas été confirmé comme envoyé. "
                "La commande reste en brouillon."
            )
            return redirect("detail_achat", id=achat.id)

    except Exception:
        messages.error(
            request,
            "L'envoi de l'e-mail a échoué. Vérifiez la configuration "
            "SMTP et l'adresse e-mail du fournisseur. "
            "La commande reste en brouillon."
        )
        return redirect("detail_achat", id=achat.id)

    # Le statut change uniquement après l'envoi réussi
    achat.montant_total = total
    achat.statut = "ENVOYE"
    achat.save(update_fields=["montant_total", "statut"])

    messages.success(
        request,
        f"La commande n°{achat.id} a été envoyée par e-mail "
        f"à {fournisseur.email}."
    )

    return redirect("detail_achat", id=achat.id)

def modifier_achat(request, id):
    achat = get_object_or_404(Achat, id=id)

    if achat.statut != "ENVOYE":
        messages.warning(
            request,
            "Cet achat n'est plus en attente de réponse du fournisseur."
        )
        return redirect("detail_achat", id=achat.id)

    if request.method == "POST":
        form = AchatForm(request.POST, instance=achat)
        formset = LigneAchatFormSet(
            request.POST,
            instance=achat
        )

        if form.is_valid() and formset.is_valid():
            achat = form.save(commit=False)

            # Ne jamais annuler ni valider la commande
            # lors de l'enregistrement de la réponse.
            achat.statut = "ENVOYE"
            achat.save()

            formset.instance = achat
            formset.save()

            achat.calculer_montant_total()

            messages.success(
                request,
                "La réponse du fournisseur a été enregistrée avec succès."
            )

            return redirect("detail_achat", id=achat.id)

        messages.error(
            request,
            "L'enregistrement a échoué. Vérifiez les erreurs affichées."
        )

    else:
        form = AchatForm(instance=achat)
        formset = LigneAchatFormSet(instance=achat)

    return render(
        request,
        "achats/ajouter.html",
        {
            "form": form,
            "formset": formset,
            "achat": achat,
            "mode_modification": True,
        }
    )


def valider_commande(request, id):
    if request.method != "POST":
        return redirect("detail_achat", id=id)

    achat = get_object_or_404(Achat, id=id)

    if achat.statut != "ENVOYE":
        messages.warning(
            request,
            "Seul un achat envoyé au fournisseur peut être validé."
        )
        return redirect("detail_achat", id=achat.id)

    if not achat.lignes.exists():
        messages.error(
            request,
            "Impossible de valider une commande sans produit."
        )
        return redirect("detail_achat", id=achat.id)

    achat.calculer_montant_total()
    achat.statut = "COMMANDE"
    achat.save(update_fields=["statut"])

    messages.success(
        request,
        "La commande fournisseur a été validée."
    )

    return redirect("detail_achat", id=achat.id)


