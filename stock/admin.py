from django.contrib import admin
from .models import LotStock
from .models import Stock, MouvementStock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'produit',
        'quantite_disponible',
        'seuil_alerte',
        'date_mise_a_jour',
    )


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = (
        'produit',
        'type_mouvement',
        'quantite',
        'motif',
        'date_mouvement',
    )

    list_filter = (
        'type_mouvement',
        'date_mouvement',
    )

    search_fields = (
        'produit__nom',
        'motif',
    )
@admin.register(LotStock)
class LotStockAdmin(admin.ModelAdmin):
    list_display = (
        'numero_lot',
        'produit',
        'quantite',
        'date_peremption'
    )    