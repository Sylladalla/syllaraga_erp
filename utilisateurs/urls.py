
from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.liste_utilisateurs,
        name="liste_utilisateurs"
    ),

    path(
        "creer/",
        views.creer_utilisateur,
        name="creer_utilisateur"
    ),

    path(
        "connexion/",
        views.connexion,
        name="connexion"
    ),

    path(
        "deconnexion/",
        views.deconnexion,
        name="deconnexion"
    ),


# utilisateurs/urls.py (Ligne 33)
# Remplacez views.dashboard_magasinier par votre vue globale (ex: views.dashboard)
path('magasin/dashboard/', views.dashboard, name='dashboard_magasinier'),




]