
from django.urls import path
from .views import imprimer_facture, liste_factures
from django.urls import path

from .views import (
    imprimer_facture,
    liste_factures,
    detail_facture
)

urlpatterns = [

    path(
        "",
        liste_factures,
        name="liste_factures"
    ),

    path(
        "facture/<int:facture_id>/pdf/",
        imprimer_facture,
        name="imprimer_facture"
    ),
path(
    "facture/<int:facture_id>/",
    detail_facture,
    name="detail_facture"
),
]