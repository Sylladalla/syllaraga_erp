#from django.db import models

# Create your models here.
from django.db import models
from ventes.models import Vente


class Facture(models.Model):

    STATUTS = (
        ('BROUILLON', 'Brouillon'),
        ('EMISE', 'Émise'),
        ('ANNULEE', 'Annulée'),
    )

    numero = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    vente = models.OneToOneField(
        Vente,
        on_delete=models.CASCADE,
        related_name='facture'
    )

    date_facture = models.DateTimeField(
        auto_now_add=True
    )

    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='BROUILLON'
    )

    def save(self, *args, **kwargs):

        # Récupération automatique du montant de la vente
        self.montant_total = self.vente.montant_total

        # Génération automatique du numéro de facture
        if not self.numero:
            dernier_id = Facture.objects.count() + 1
            self.numero = f"FAC-{dernier_id:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero