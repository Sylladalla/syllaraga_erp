from datetime import datetime
from stock.models import LotStock, MouvementStock, Stock
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from django.db import models
from .models import Stock, LotStock


def generer_numero_lot():
    date = datetime.now().strftime("%Y%m%d")

    nombre = LotStock.objects.count() + 1

    return f"LOT-{date}-{nombre:03d}"


def sortir_du_stock(produit, quantite, motif="Vente"):

    # Vérification de la quantité demandée
    if quantite <= 0:
        raise ValueError(
            "La quantité doit être supérieure à zéro."
        )

    # Récupérer le stock global
    stock = Stock.objects.get(
        produit=produit
    )

    # Vérifier le stock global
    if stock.quantite_disponible < quantite:
        raise ValueError(
            f"Stock insuffisant pour {produit.nom}. "
            f"Disponible : {stock.quantite_disponible}, "
            f"demandé : {quantite}."
        )

    # Récupérer les lots disponibles selon FEFO
    lots = list(
        LotStock.objects.filter(
            produit=produit,
            quantite__gt=0
        ).order_by(
            "date_peremption"
        )
    )

    # Vérifier la quantité disponible dans les lots
    total_lots = sum(
        lot.quantite for lot in lots
    )

    if total_lots < quantite:
        raise ValueError(
            f"Stock par lots insuffisant pour {produit.nom}. "
            f"Disponible dans les lots : {total_lots}, "
            f"demandé : {quantite}."
        )

    quantite_restante = quantite

    # Sortie selon FEFO
    for lot in lots:

        if quantite_restante <= 0:
            break

        quantite_a_retirer = min(
            lot.quantite,
            quantite_restante
        )

        lot.quantite -= quantite_a_retirer

        quantite_restante -= quantite_a_retirer

        lot.save()

    # Le mouvement mettra automatiquement à jour
    # le stock global
    MouvementStock.objects.create(
        produit=produit,
        type_mouvement="SORTIE",
        quantite=quantite,
        motif=motif
    )
def lots_a_peremption_proche(jours=7):
    """
    Retourne les lots qui expirent dans les 'jours' prochains.
    """

    aujourd_hui = timezone.now().date()
    date_limite = aujourd_hui + timedelta(days=jours)

    return LotStock.objects.filter(
        date_peremption__gte=aujourd_hui,
        date_peremption__lte=date_limite,
        quantite__gt=0
    ).order_by('date_peremption')
def lots_perimes():
    """
    Retourne les lots déjà périmés.
    """

    aujourd_hui = timezone.now().date()

    return LotStock.objects.filter(
        date_peremption__lt=aujourd_hui,
        quantite__gt=0
    ).order_by('date_peremption')
def stocks_faibles():
    return Stock.objects.filter(
        quantite_disponible__gt=0,
        quantite_disponible__lte=models.F("seuil_alerte")
    )           