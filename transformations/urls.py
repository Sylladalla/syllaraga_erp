from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.liste_transformations,
        name="liste_transformations"
    ),

    path(
        "creer/",
        views.creer_transformation,
        name="creer_transformation"
    ),

    path(
        "<int:id>/",
        views.detail_transformation,
        name="detail_transformation"
    ),

    path(
        "<int:id>/terminer/",
        views.terminer_transformation,
        name="terminer_transformation"
    ),

    path(
        "<int:id>/annuler/",
        views.annuler_transformation,
        name="annuler_transformation"
    ),

]