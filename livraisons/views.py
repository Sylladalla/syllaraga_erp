from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LivraisonForm, ZoneLivraisonForm
from .models import Livraison, ZoneLivraison
from ventes.models import Vente
from utilisateurs.decorators import role_requis


@role_requis(["ADMIN"])
def gerer_livraison(request, vente_id):
    vente = get_object_or_404(
        Vente,
        id=vente_id
    )

    # Une livraison concerne uniquement une vente en ligne
    if vente.type_vente != "EN_LIGNE":

        messages.error(
            request,
            "Cette vente ne nécessite pas de livraison."
        )

        return redirect(
            "detail_vente",
            id=vente.id
        )

    # Récupérer ou créer la livraison
    livraison, created = Livraison.objects.get_or_create(
        vente=vente,
        defaults={
            "adresse_livraison": vente.client.adresse
        }
    )

    if request.method == "POST":

        form = LivraisonForm(
            request.POST,
            instance=livraison
        )

        if form.is_valid():

            livraison = form.save()

            messages.success(
                request,
                "La livraison a été enregistrée avec succès."
            )

            return redirect(
                "detail_livraison",
                livraison.id
            )

    else:

        form = LivraisonForm(
            instance=livraison
        )

    return render(
        request,
        "livraisons/gerer.html",
        {
            "vente": vente,
            "livraison": livraison,
            "form": form
        }
    )


@role_requis(["ADMIN", "LIVREUR"])
def detail_livraison(request, id):
    livraison = get_object_or_404(
        Livraison,
        id=id
    )

    return render(
        request,
        "livraisons/detail.html",
        {
            "livraison": livraison
        }
    )
@role_requis(["ADMIN", "LIVREUR"])
def demarrer_livraison(request, id):
    livraison = get_object_or_404(
        Livraison,
        id=id
    )

    if request.method == "POST":

        try:

            livraison.demarrer()

            messages.success(
                request,
                "La livraison est maintenant en cours."
            )

        except ValueError as e:

            messages.error(
                request,
                str(e)
            )

    return redirect(
        "detail_livraison",
        id=livraison.id
    )


@role_requis(["ADMIN", "LIVREUR"])
def terminer_livraison(request, id):
    livraison = get_object_or_404(
        Livraison,
        id=id
    )

    if request.method == "POST":

        try:

            livraison.livrer()

            messages.success(
                request,
                "La livraison a été marquée comme livrée."
            )

        except ValueError as e:

            messages.error(
                request,
                str(e)
            )

    return redirect(
        "detail_livraison",
        id=livraison.id
    )


@role_requis(["ADMIN"])
def annuler_livraison(request, id):
    livraison = get_object_or_404(
        Livraison,
        id=id
    )

    if request.method == "POST":

        try:

            livraison.annuler()

            messages.success(
                request,
                "La livraison a été annulée."
            )

        except ValueError as e:

            messages.error(
                request,
                str(e)
            )

    return redirect(
        "detail_livraison",
        id=livraison.id
    )    
@role_requis(["ADMIN"])
def liste_zones(request):
    zones = ZoneLivraison.objects.all().order_by("nom")

    return render(
        request,
        "livraisons/liste_zones.html",
        {
            "zones": zones
        }
    )


@role_requis(["ADMIN"])
def ajouter_zone(request):
    if request.method == "POST":

        form = ZoneLivraisonForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "La zone de livraison a été ajoutée avec succès."
            )

            return redirect("liste_zones")

    else:

        form = ZoneLivraisonForm()

    return render(
        request,
        "livraisons/ajouter_zone.html",
        {
            "form": form
        }
    )


@role_requis(["ADMIN"])
def modifier_zone(request, id):
    zone = get_object_or_404(
        ZoneLivraison,
        id=id
    )

    if request.method == "POST":

        form = ZoneLivraisonForm(
            request.POST,
            instance=zone
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "La zone de livraison a été modifiée avec succès."
            )

            return redirect("liste_zones")

    else:

        form = ZoneLivraisonForm(
            instance=zone
        )

    return render(
        request,
        "livraisons/modifier_zone.html",
        {
            "form": form,
            "zone": zone
        }
    )


@role_requis(["ADMIN"])
def supprimer_zone(request, id):
    zone = get_object_or_404(
        ZoneLivraison,
        id=id
    )

    if request.method == "POST":

        try:

            zone.delete()

            messages.success(
                request,
                "La zone de livraison a été supprimée avec succès."
            )

        except Exception:

            messages.error(
                request,
                "Impossible de supprimer cette zone car elle est utilisée par une livraison."
            )

        return redirect("liste_zones")

    return render(
        request,
        "livraisons/supprimer_zone.html",
        {
            "zone": zone
        }
    )  
@role_requis(roles=['ADMINISTRATEUR', 'LIVREUR'])
def liste_livraisons(request):
    livraisons = Livraison.objects.select_related(
        "vente",
        "vente__client",
        "zone"
    ).order_by(
        "-id"
    )

    return render(
        request,
        "livraisons/liste.html",
        {
            "livraisons": livraisons
        }
    )      