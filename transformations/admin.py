from django.contrib import admin
from .models import Transformation, LigneTransformation


class LigneTransformationInline(admin.TabularInline):
    model = LigneTransformation
    extra = 1


@admin.register(Transformation)
class TransformationAdmin(admin.ModelAdmin):

    list_display = (
        'produit',
        'quantite_produite',
        'date_transformation',
        'statut',
    )

    list_filter = (
        'statut',
        'date_transformation',
    )

    search_fields = (
        'produit__nom',
    )

    ordering = (
        '-date_transformation',
    )

    inlines = [LigneTransformationInline]
    actions = ['terminer_transformations']


    def terminer_transformations(self, request, queryset):

        for transformation in queryset:
            transformation.terminer()

        self.message_user(
            request,
            "Les transformations sélectionnées ont été terminées."
        )


    terminer_transformations.short_description = (
        "Terminer les transformations sélectionnées"
    )