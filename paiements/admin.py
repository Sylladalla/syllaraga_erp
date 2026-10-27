from django.contrib import admin
from .models import Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):

    list_display = (
        'vente',
        'montant',
        'mode_paiement',
        'statut',
        'date_paiement',
    )

    list_filter = (
        'mode_paiement',
        'statut',
        'date_paiement',
    )

    search_fields = (
        'vente__id',
        'vente__client__nom',
    )

    readonly_fields = (
        'montant',
    )

    actions = ['effectuer_paiements']

    def effectuer_paiements(self, request, queryset):

        for paiement in queryset:
            paiement.effectuer()

        self.message_user(
            request,
            "Les paiements sélectionnés ont été effectués."
        )

    effectuer_paiements.short_description = (
        "Effectuer les paiements sélectionnés"
    )