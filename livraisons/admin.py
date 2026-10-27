
from django.contrib import admin

from .models import Livraison, ZoneLivraison


@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):

    list_display = (
        'vente',
        'statut',
        'zone',
        'livreur',
        'telephone_livreur',
        'date_livraison',
    )

    list_filter = (
        'statut',
        'zone',
        'date_livraison',
    )

    search_fields = (
        'vente__client__nom',
        'vente__client__prenom',
        'livreur',
        'telephone_livreur',
        'adresse_livraison',
    )

    ordering = (
        '-date_livraison',
    )

    actions = [
        'marquer_livrees'
    ]

    @admin.action(
        description="Marquer les livraisons sélectionnées comme livrées"
    )
    def marquer_livrees(self, request, queryset):

        for livraison in queryset:

            livraison.livrer()

        self.message_user(
            request,
            "Les livraisons sélectionnées sont maintenant livrées."
        )


@admin.register(ZoneLivraison)
class ZoneLivraisonAdmin(admin.ModelAdmin):

    list_display = (
        'nom',
        'frais',
    )

    search_fields = (
        'nom',
    )