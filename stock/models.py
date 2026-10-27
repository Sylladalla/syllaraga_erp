#from django.db import models

# Create your models here.
from django.db import models
from produits.models import Produit


class Stock(models.Model):
    produit = models.OneToOneField(
        Produit,
        on_delete=models.CASCADE,
        related_name='stock'
    )

    quantite_disponible = models.PositiveIntegerField(default=0)

    seuil_alerte = models.PositiveIntegerField(default=10)

    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produit.nom} - {self.quantite_disponible}"
        ##
class MouvementStock(models.Model):

    TYPES_MOUVEMENT = (
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='mouvements_stock'
    )

    type_mouvement = models.CharField(
        max_length=10,
        choices=TYPES_MOUVEMENT
    )

    quantite = models.PositiveIntegerField()

    date_mouvement = models.DateTimeField(auto_now_add=True)

    motif = models.CharField(
        max_length=100
    )
    #entree sortie#
    def save(self, *args, **kwargs):

        stock, created = Stock.objects.get_or_create(
            produit=self.produit
        )

        if self.type_mouvement == 'ENTREE':
            stock.quantite_disponible += self.quantite

        elif self.type_mouvement == 'SORTIE':

            if stock.quantite_disponible < self.quantite:
                raise ValueError(
                    "Stock insuffisant pour effectuer cette sortie."
                )

            stock.quantite_disponible -= self.quantite

        stock.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"

class LotStock(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name="lots",
        verbose_name="Produit"
    )

    numero_lot = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro du lot"
    )

    quantite = models.PositiveIntegerField(
        verbose_name="Quantité disponible"
    )

    prix_achat_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix d'achat unitaire"
    )

    date_entree = models.DateField(
        auto_now_add=True,
        verbose_name="Date d'entrée"
    )

    date_peremption = models.DateField(
        verbose_name="Date de péremption"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['date_peremption']
        verbose_name = "Lot de stock"
        verbose_name_plural = "Lots de stock"

    def __str__(self):
        return f"{self.numero_lot} - {self.produit.nom}"        