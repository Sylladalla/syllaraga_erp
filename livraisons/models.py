#from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from ventes.models import Vente


class Livraison(models.Model):

    STATUTS = (
        ('EN_PREPARATION', 'En préparation'),
        ('EN_COURS', 'En cours de livraison'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    )

    vente = models.OneToOneField(
        Vente,
        on_delete=models.CASCADE,
        related_name='livraison'
    )

    adresse_livraison = models.TextField()

    date_livraison = models.DateTimeField(
        null=True,
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='EN_PREPARATION'
    )

    livreur = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    telephone_livreur = models.CharField(
        max_length=20,
        blank=True,
        null=True
)    
    zone = models.ForeignKey(
    'ZoneLivraison',
        on_delete=models.PROTECT,
        null=True,
        blank=True
)
    def demarrer(self):
        if self.statut != "EN_PREPARATION":
            raise ValueError(
                "Cette livraison ne peut pas encore démarrer."
            )

        self.statut = "EN_COURS"
        self.save(update_fields=["statut"])


    def livrer(self):
        if self.statut != "EN_COURS":
            raise ValueError(
                "La livraison doit être en cours avant d'être marquée comme livrée."
            )

        self.statut = "LIVREE"
        self.date_livraison = timezone.now()

        self.save(
            update_fields=[
                "statut",
                "date_livraison"
            ]
        )


    def annuler(self):
        if self.statut == "LIVREE":
            raise ValueError(
                "Une livraison déjà effectuée ne peut pas être annulée."
            )

        self.statut = "ANNULEE"
        self.save(update_fields=["statut"])

    def save(self, *args, **kwargs):

        if self.zone:
            self.vente.frais_livraison = self.zone.frais

            total_produits = sum(
                ligne.quantite * ligne.prix_unitaire
                for ligne in self.vente.lignes.all()
            )

            self.vente.montant_total = (
                total_produits + self.zone.frais
            )

            self.vente.save()

        super().save(*args, **kwargs)
    def __str__(self):
        return f"Livraison {self.id} - {self.vente.client.nom}"  

class ZoneLivraison(models.Model):

    nom = models.CharField(
        max_length=100,
        unique=True
    )

    frais = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.nom} - {self.frais} FCFA"

    
 
    