
from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.liste_paiements,
        name="liste_paiements"
    ),

    path(
        "vente/<int:vente_id>/effectuer/",
        views.effectuer_paiement,
        name="effectuer_paiement"
    ),

    path(
        "<int:id>/",
        views.detail_paiement,
        name="detail_paiement"
    ),
path(
    "fournisseur/achat/<int:achat_id>/",
    views.payer_fournisseur,
    name="paiement_fournisseur",
),

path(
    "fournisseur/reglement/<int:paiement_id>/",
    views.detail_paiement_fournisseur,
    name="detail_paiement_fournisseur",
),
]