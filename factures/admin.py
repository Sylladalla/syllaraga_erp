from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Facture


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):

    list_display = (
        'numero',
        'vente',
        'date_facture',
        'montant_total',
        'statut',
        'imprimer_facture',
    )

    list_filter = (
        'statut',
        'date_facture',
    )

    search_fields = (
        'numero',
        'vente__client__nom',
        'vente__client__prenom',
    )

    ordering = (
        '-date_facture',
    )

    readonly_fields = (
        'numero',
        'montant_total',
        'date_facture',
        'imprimer_facture',
    )

    def imprimer_facture(self, obj):

        url = reverse(
            'imprimer_facture',
            args=[obj.id]
        )

        return format_html(
            '<a class="button" href="{}" target="_blank">🖨️ Imprimer</a>',
            url
        )

    imprimer_facture.short_description = "Facture PDF"