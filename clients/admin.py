#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = (
        'nom',
        'prenom',
        'telephone',
        'email',
        'date_creation',
    )

    search_fields = (
        'nom',
        'prenom',
        'telephone',
    )

    list_filter = (
        'date_creation',
    )

    ordering = (
        'nom',
        'prenom',
    )