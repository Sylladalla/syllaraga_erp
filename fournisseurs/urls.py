from django.urls import path

from . import views


urlpatterns = [

    path(
        "ajouter/",
        views.ajouter_fournisseur,
        name="ajouter_fournisseur"
    ),


    path(
        "",
        views.liste_fournisseurs,
        name="liste_fournisseurs"
    ),


    path(
        "<int:id>/",
        views.detail_fournisseur,
        name="detail_fournisseur"
    ),

]