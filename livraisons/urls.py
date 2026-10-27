
from django.urls import path
from . import views


urlpatterns = [

    # Livraison
    path(
        "vente/<int:vente_id>/",
        views.gerer_livraison,
        name="gerer_livraison"
    ),

    path(
        "<int:id>/",
        views.detail_livraison,
        name="detail_livraison"
    ),


    # Zones de livraison
    path(
        "zones/",
        views.liste_zones,
        name="liste_zones"
    ),

    path(
        "zones/ajouter/",
        views.ajouter_zone,
        name="ajouter_zone"
    ),

    path(
        "zones/<int:id>/modifier/",
        views.modifier_zone,
        name="modifier_zone"
    ),

    path(
        "zones/<int:id>/supprimer/",
        views.supprimer_zone,
        name="supprimer_zone"
    ),
    path(
    "liste/",
    views.liste_livraisons,
    name="liste_livraisons"
),
path(
    "<int:id>/demarrer/",
    views.demarrer_livraison,
    name="demarrer_livraison"
),

path(
    "<int:id>/terminer/",
    views.terminer_livraison,
    name="terminer_livraison"
),

path(
    "<int:id>/annuler/",
    views.annuler_livraison,
    name="annuler_livraison"
),

]