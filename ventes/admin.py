from django.contrib import admin
from .models import Vente, LigneVente


class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 1


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'client',
        'type_vente',
        'date_vente',
        'statut',
        'frais_livraison',
        'montant_total',
    )

    list_filter = (
        'type_vente',
        'statut',
        'date_vente',
    )

    inlines = [LigneVenteInline]

    actions = ['confirmer_ventes']


    def confirmer_ventes(self, request, queryset):

        for vente in queryset:
            vente.confirmer()

        self.message_user(
            request,
            "Les ventes sélectionnées ont été confirmées."
        )


    confirmer_ventes.short_description = "Confirmer les ventes sélectionnées"