from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.accueil,
        name="accueil"
    ),
     path(
        "produit/<int:produit_id>/",
        views.detail_produit,
        name="detail_produit"
    ),
    path(
    "panier/",
    views.panier,
    name="panier"
),
path(
    "panier/ajouter/<int:produit_id>/",
    views.ajouter_au_panier,
    name="ajouter_au_panier"
),
path(
    "panier/augmenter/<int:produit_id>/",
    views.augmenter_quantite,
    name="augmenter_quantite"
),
path(
    "panier/diminuer/<int:produit_id>/",
    views.diminuer_quantite,
    name="diminuer_quantite"
),
  path(
        "panier/modifier/<int:produit_id>/",
        views.modifier_quantite_panier,
        name="modifier_quantite_panier"
    ),
path(
    "panier/supprimer/<int:produit_id>/",
    views.supprimer_du_panier,
    name="supprimer_du_panier"
),
path(
    "commande/",
    views.passer_commande,
    name="passer_commande"
),
path(
    "mes-commandes/",
    views.mes_commandes,
    name="mes_commandes"
),
path(
    "mes-commandes/<int:vente_id>/",
    views.detail_commande,
    name="detail_commande"
),
path(
    "commande/<int:vente_id>/payer/",
    views.payer_commande,
    name="payer_commande"
),
path(
    "paydunya/ipn/",
    views.paydunya_ipn,
    name="paydunya_ipn"
),


path(
    "paydunya/retour/<int:vente_id>/",
    views.paydunya_retour,
    name="paydunya_retour"
),

path(
    "paydunya/annulation/<int:vente_id>/",
    views.paydunya_annulation,
    name="paydunya_annulation"
),
path(
    "livraison/zone/",
    views.choisir_zone_livraison,
    name="choisir_zone_livraison"
),

# path(
#     "paiement/cinetpay/notification/",
#     views.paiement_cinetpay_notification,
#     name="paiement_cinetpay_notification"
# ),

# path(
#     "paiement/cinetpay/retour/<int:vente_id>/",
#     views.paiement_cinetpay_retour,
#     name="paiement_cinetpay_retour"
# ),


]