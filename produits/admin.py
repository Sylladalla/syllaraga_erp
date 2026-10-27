#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categorie, Produit


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'categorie',
        'type_produit',
        'prix_achat',
        'prix_vente',
        'est_perissable'
    )

    list_filter = (
        'categorie',
        'type_produit',
        'est_perissable'
    )

    search_fields = ('nom',)