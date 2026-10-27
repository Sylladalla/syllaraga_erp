
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ventes.models import Vente
from .models import Paiement
from .forms import PaiementForm
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from achats.models import Achat
from .models import PaiementFournisseur
from .forms import PaiementFournisseurForm

def effectuer_paiement(request, vente_id):

    vente = get_object_or_404(
        Vente,
        id=vente_id
    )

    # La vente doit être confirmée
    if vente.statut != "CONFIRMEE":

        messages.error(
            request,
            "Impossible d'effectuer un paiement pour une vente non confirmée."
        )

        return redirect(
            "detail_vente",
            id=vente.id
        )

    # Récupérer ou créer le paiement
    paiement, created = Paiement.objects.get_or_create(
        vente=vente,
        defaults={
            "montant": vente.montant_total,
            "mode_paiement": "ESPECES"
        }
    )

    if request.method == "POST":

        form = PaiementForm(
            request.POST,
            instance=paiement
        )

        if form.is_valid():

            paiement = form.save()

            paiement.effectuer()

            messages.success(
                request,
                "Le paiement a été effectué avec succès."
            )

            return redirect(
                "detail_paiement",
                paiement.id
            )

    else:

        form = PaiementForm(
            instance=paiement
        )

    return render(
        request,
        "paiements/effectuer.html",
        {
            "vente": vente,
            "paiement": paiement,
            "form": form
        }
    )


def detail_paiement(request, id):

    paiement = get_object_or_404(
        Paiement,
        id=id
    )

    return render(
        request,
        "paiements/detail.html",
        {
            "paiement": paiement
        }
    )
def liste_paiements(request):

    paiements = Paiement.objects.select_related(
        "vente"
    ).order_by("-date_paiement")

    return render(
        request,
        "paiements/liste.html",
        {
            "paiements": paiements
        }
    )    

def payer_fournisseur(request, achat_id):
    achat = get_object_or_404(Achat, id=achat_id)

    if achat.statut != "RECEPTIONNE":
        messages.error(
            request,
            "Le paiement est autorisé uniquement après réception de l'achat."
        )
        return redirect("detail_achat", id=achat.id)

    paiements = PaiementFournisseur.objects.filter(
        achat=achat
    ).order_by("-date_paiement")

    montant_paye = sum(
        (p.montant for p in paiements),
        Decimal("0.00")
    )
    reste_a_payer = achat.montant_total - montant_paye

    if reste_a_payer <= 0:
        messages.info(
            request,
            "Cet achat fournisseur est déjà entièrement payé."
        )
        return redirect("detail_achat", id=achat.id)

    if request.method == "POST":
        form = PaiementFournisseurForm(request.POST)

        if form.is_valid():
            montant = form.cleaned_data["montant"]

            # Vérification du solde juste avant l'enregistrement.
            with transaction.atomic():
                paiements_actuels = PaiementFournisseur.objects.filter(
                    achat=achat
                ).select_for_update()

                montant_actuel = sum(
                    (p.montant for p in paiements_actuels),
                    Decimal("0.00")
                )
                solde_actuel = achat.montant_total - montant_actuel

                if montant > solde_actuel:
                    form.add_error(
                        "montant",
                        f"Le montant dépasse le reste à payer "
                        f"({solde_actuel:.2f})."
                    )
                else:
                    paiement = form.save(commit=False)
                    paiement.achat = achat
                    paiement.save()

                    messages.success(
                        request,
                        "Le paiement fournisseur a été enregistré."
                    )
                    return redirect(
                        "paiement_fournisseur",
                        achat_id=achat.id
                    )

    else:
        form = PaiementFournisseurForm()

    return render(
        request,
        "paiements/fournisseur.html",
        {
            "achat": achat,
            "form": form,
            "paiements": paiements,
            "montant_paye": montant_paye,
            "reste_a_payer": reste_a_payer,
        }
    )


def detail_paiement_fournisseur(request, paiement_id):
    paiement = get_object_or_404(
        PaiementFournisseur.objects.select_related(
            "achat",
            "achat__fournisseur",
        ),
        id=paiement_id,
    )

    return render(
        request,
        "paiements/detail_fournisseur.html",
        {"paiement": paiement},
    )
