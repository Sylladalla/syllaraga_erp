

from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):

    ROLES = (
        ('ADMIN', 'Administrateur'),
        ('STOCK', 'Responsable stock'),
        ('MAGASINIER', 'Magasinier'),
        ('VENDEUR', 'Vendeur'),
        ('EMPLOYE', 'Employé'),
        ('LIVREUR', 'Livreur'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='EMPLOYE'
    )

    telephone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
