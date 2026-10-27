

import secrets

from django.db import models
from django.utils import timezone


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    telephone = models.CharField(
        max_length=20,
        unique=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
    )

    # Le mot de passe sera stocké sous forme hachée.
    mot_de_passe = models.CharField(max_length=128)

    adresse = models.TextField(blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    # Champs nécessaires à la réinitialisation du mot de passe.
    token_reinitialisation = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )

    token_expiration = models.DateTimeField(
        blank=True,
        null=True,
    )

    def generer_token_reinitialisation(self):
        self.token_reinitialisation = secrets.token_urlsafe(32)
        self.token_expiration = timezone.now() + timezone.timedelta(hours=1)
        self.save(
            update_fields=[
                "token_reinitialisation",
                "token_expiration",
            ]
        )
        return self.token_reinitialisation

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["nom", "prenom"]
