from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations ERP', {
            'fields': ('role', 'telephone'),
        }),
    )