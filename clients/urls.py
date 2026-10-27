

from django.urls import path

from . import views


urlpatterns = [
    path(
        "inscription/",
        views.inscription_client,
        name="inscription_client",
    ),
    path(
        "connexion/",
        views.connexion_client,
        name="connexion_client",
    ),
    path(
        "accueil/",
        views.accueil_clients,
        name="accueil_clients",
    ),
    path(
        "deconnexion/",
        views.deconnexion_client,
        name="deconnexion_client",
    ),
    path(
        "mot-de-passe-oublie/",
        views.mot_de_passe_oublie,
        name="mot_de_passe_oublie",
    ),
    path(
        "reinitialiser-mot-de-passe/<str:token>/",
        views.reinitialiser_mot_de_passe,
        name="reinitialiser_mot_de_passe",
    ),
]
