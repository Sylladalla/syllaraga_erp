from django.contrib import admin
from .models import Achat, LigneAchat


class LigneAchatInline(admin.TabularInline):
    model = LigneAchat
    extra = 1


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'fournisseur',
        'date_achat',
        'statut',
        'montant_total',
    )
    readonly_fields = ('montant_total',)
    list_filter = (
        'statut',
        'date_achat',
    )

    inlines = [LigneAchatInline]


    actions = ['receptionner_achats']


    def receptionner_achats(self, request, queryset):
        for achat in queryset:
            achat.receptionner()

        self.message_user(
            request,
            "Les achats sélectionnés ont été réceptionnés."
        )


    receptionner_achats.short_description = "Réceptionner les achats sélectionnés"