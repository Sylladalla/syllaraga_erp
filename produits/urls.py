from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.liste_produits,
        name="liste_produits"
    ),
path(
    "ajouter/",
    views.ajouter_produit,
    name="ajouter_produit"
),
path(
    "categorie/ajouter/",
    views.ajouter_categorie,
    name="ajouter_categorie"
),
path(
    "categories/",
    views.liste_categories,
    name="liste_categories"
),
path(
    "modifier/<int:id>/",
    views.modifier_produit,
    name="modifier_produit"
),
path(
    "supprimer/<int:id>/",
    views.supprimer_produit,
    name="supprimer_produit"
),
path(
    "categories/",
    views.liste_categories,
    name="liste_categories"
),
path(
    "categories/modifier/<int:id>/",
    views.modifier_categorie,
    name="modifier_categorie"
),
path(
    "categories/supprimer/<int:id>/",
    views.supprimer_categorie,
    name="supprimer_categorie"
),
]