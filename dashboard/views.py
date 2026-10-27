
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from utilisateurs.decorators import role_requis
from produits.models import Produit
from ventes.models import Vente
from achats.models import Achat
from transformations.models import Transformation
from stock.models import Stock
from fournisseurs.models import Fournisseur
from stock.services import (
    stocks_faibles,
    lots_a_peremption_proche,
    lots_perimes
)


@role_requis(["ADMIN"])
def dashboard(request):

    # =====================================================
    # STATISTIQUES GENERALES
    # =====================================================

    nombre_produits = Produit.objects.count()

    nombre_ventes = Vente.objects.count()

    nombre_achats = Achat.objects.count()
    nombre_fournisseurs = Fournisseur.objects.count()


    # =====================================================
    # STOCK
    # =====================================================

    produits_stock_faible = stocks_faibles()

    nombre_stocks_faibles = produits_stock_faible.count()


    nombre_ruptures = Stock.objects.filter(
        quantite_disponible=0
    ).count()


    # =====================================================
    # PEREMPTION
    # =====================================================

    produits_proches_peremption = lots_a_peremption_proche()

    produits_perimes = lots_perimes()


    nombre_lots_proches = produits_proches_peremption.count()

    nombre_lots_perimes = produits_perimes.count()


    # =====================================================
    # CHIFFRE D'AFFAIRES
    # =====================================================

    chiffre_affaires = Vente.objects.filter(
        statut="CONFIRMEE"
    ).aggregate(
        total=Sum("montant_total")
    )["total"] or 0


    # =====================================================
    # VENTES BOUTIQUE / EN LIGNE
    # =====================================================

    ventes_par_type = Vente.objects.values(
        "type_vente"
    ).annotate(
        total=Count("id")
    )


    # =====================================================
    # EVOLUTION DU CHIFFRE D'AFFAIRES
    # =====================================================

    ventes_par_mois = Vente.objects.filter(
        statut="CONFIRMEE"
    ).annotate(
        mois=TruncMonth("date_vente")
    ).values(
        "mois"
    ).annotate(
        total=Sum("montant_total")
    ).order_by(
        "mois"
    )


    # =====================================================
    # TRANSFORMATIONS
    # =====================================================

    nombre_transformations = Transformation.objects.filter(
        statut="TERMINEE"
    ).count()


    quantite_produite = Transformation.objects.filter(
        statut="TERMINEE"
    ).aggregate(
        total=Sum("quantite_produite")
    )["total"] or 0


    # =====================================================
    # BENEFICE ESTIME
    # =====================================================

    total_achats = Achat.objects.filter(
        statut="RECEPTIONNE"
    ).aggregate(
        total=Sum("montant_total")
    )["total"] or 0


    benefice = chiffre_affaires - total_achats


    # =====================================================
    # DONNEES GRAPHIQUE STOCK FAIBLE
    # =====================================================

    stock_graphique = []

    for stock in produits_stock_faible:

        stock_graphique.append({
            "produit": stock.produit.nom,
            "quantite": stock.quantite_disponible
        })


    # =====================================================
    # DONNEES GRAPHIQUE TRANSFORMATIONS
    # =====================================================

    transformations_graphique = Transformation.objects.filter(
        statut="TERMINEE"
    ).values(
        "produit__nom"
    ).annotate(
        total=Sum("quantite_produite")
    )


    # =====================================================
    # CONTEXTE
    # =====================================================

    contexte = {

        # Général
        "nombre_produits": nombre_produits,
        "nombre_ventes": nombre_ventes,
        "nombre_achats": nombre_achats,
        "nombre_fournisseurs": nombre_fournisseurs,

        # Stock
        "stocks_faibles": produits_stock_faible,
        "nombre_stocks_faibles": nombre_stocks_faibles,
        "nombre_ruptures": nombre_ruptures,

        # Péremption
        "lots_proches": produits_proches_peremption,
        "lots_perimes": produits_perimes,
        "nombre_lots_proches": nombre_lots_proches,
        "nombre_lots_perimes": nombre_lots_perimes,

        # Finances
        "chiffre_affaires": chiffre_affaires,
        "total_achats": total_achats,
        "benefice": benefice,

        # Ventes
        "ventes_par_type": ventes_par_type,
        "ventes_par_mois": ventes_par_mois,

        # Transformations
        "nombre_transformations": nombre_transformations,
        "quantite_produite": quantite_produite,

        # Graphiques
        "stock_graphique": stock_graphique,
        "transformations_graphique": transformations_graphique,
    }


    return render(
        request,
        "dashboard/dashboard.html",
        contexte
    )