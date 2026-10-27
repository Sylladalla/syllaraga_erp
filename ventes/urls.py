
from django.urls import path

from . import views


urlpatterns = [

    path(
        "ajouter/",
        views.ajouter_vente,
        name="ajouter_vente"
    ),

    path(
        "<int:id>/ajouter-ligne/",
        views.ajouter_ligne_vente,
        name="ajouter_ligne_vente"
    ),

    path(
        "<int:id>/confirmer/",
        views.confirmer_vente,
        name="confirmer_vente"
    ),
    path(
    "<int:id>/annuler/",
    views.annuler_vente,
    name="annuler_vente"
),
    path(
    "<int:id>/ajouter-produit-direct/",
    views.ajouter_produit_direct,
    name="ajouter_produit_direct"
),
    path(
        "<int:id>/",
        views.detail_vente,
        name="detail_vente"
    ),
    path(
    "",
    views.liste_ventes,
    name="liste_ventes"
),

]