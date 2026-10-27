from django.contrib import admin

# Register your models here.
#from django.contrib import admin
from .models import Fournisseur


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'telephone',
        'email',
        'date_creation',
    )

    search_fields = (
        'nom',
        'telephone',
    )