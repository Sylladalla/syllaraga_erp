from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.liste_achats,
        name="liste_achats"
    ),
path(
    "ajouter/",
    views.ajouter_achat,
    name="ajouter_achat"
), 
path(
    "<int:id>/",
    views.detail_achat,
    name="detail_achat"
),
path(
    "<int:id>/receptionner/",
    views.receptionner_achat,
    name="receptionner_achat"
),   
path(
    "<int:id>/envoyer/",
    views.envoyer_achat,
    name="envoyer_achat"
),

path(
    "<int:id>/modifier/",
    views.modifier_achat,
    name="modifier_achat"
),

path(
    "<int:id>/valider/",
    views.valider_commande,
    name="valider_commande"
),
path("<int:id>/valider/", views.valider_commande, name="valider_commande"),

]