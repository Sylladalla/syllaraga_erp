
import requests

from django.conf import settings
import socket
import urllib3.util.connection as urllib3_connection
# Utiliser IPv4 pour les connexions HTTP sortantes
urllib3_connection.allowed_gai_family = lambda: socket.AF_INET

PAYDUNYA_CREATE_URL = (
    "https://app.paydunya.com/"
    "sandbox-api/v1/checkout-invoice/create"
)


def creer_facture_paydunya(
    montant,
    description,
    callback_url,
    return_url,
    cancel_url,
    client_nom,
    client_email,
    client_telephone,
    commande,
):

    headers = {
        "Content-Type": "application/json",
        "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
        "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
        "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
    }

    # ==========================================
    # PRODUITS DE LA COMMANDE
    # ==========================================

    items = {}

    for index, ligne in enumerate(
        commande.lignes.select_related("produit")
    ):
        items[f"item_{index}"] = {
            "name": ligne.produit.nom,
            "quantity": ligne.quantite,
            "unit_price": str(ligne.prix_unitaire),
            "total_price": str(
                ligne.prix_unitaire * ligne.quantite
            ),
            "description": ligne.produit.description or "",
        }

    # ==========================================
    # FRAIS DE LIVRAISON
    # ==========================================

    taxes = {}

    if commande.frais_livraison and commande.frais_livraison > 0:

        taxes["tax_0"] = {
            "name": "Livraison",
            "amount": int(commande.frais_livraison),
        }

    # ==========================================
    # FACTURE PAYDUNYA
    # ==========================================

    payload = {
        "invoice": {

            "items": items,

            "taxes": taxes,

            "total_amount": int(montant),

            "description": description,

            "customer": {
                "name": client_nom,
                "email": client_email or "",
                "phone": client_telephone or "",
            },
        },

        "store": {
            "name": "Syllaraga",
            "tagline": "Bio pour bien manger",
        },

        "actions": {
            "callback_url": callback_url,
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
    }

    # ==========================================
    # DEBUG
    # ==========================================

    print("========== PAYDUNYA ==========")
    print("URL :", PAYDUNYA_CREATE_URL)
    print("COMMANDE :", commande.id)
    print("MONTANT :", montant)
    print("FRAIS LIVRAISON :", commande.frais_livraison)
    print("ITEMS :", items)
    print("TAXES :", taxes)
    print("CLIENT :", client_nom)
    print("EMAIL :", client_email)
    print("TELEPHONE :", client_telephone)
    print("PAYLOAD :", payload)
    print("==============================")

    response = requests.post(
        PAYDUNYA_CREATE_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("STATUS PAYDUNYA :", response.status_code)
    print("REPONSE BRUTE PAYDUNYA :", response.text)

    response.raise_for_status()

    return response.json()
def verifier_paiement_paydunya(token):

    url = (
        "https://app.paydunya.com/"
        f"sandbox-api/v1/checkout-invoice/confirm/{token}"
    )

    headers = {
        "Content-Type": "application/json",
        "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
        "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
        "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()   