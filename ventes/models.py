
from django.db import models, transaction

from produits.models import Produit
from clients.models import Client


class Vente(models.Model):

    STATUTS = (
        ('BROUILLON', 'Brouillon'),
        ('CONFIRMEE', 'Confirmée'),
        ('ANNULEE', 'Annulée'),
    )

    TYPES_VENTE = (
        ('BOUTIQUE', 'Vente boutique'),
        ('EN_LIGNE', 'Vente en ligne'),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='ventes'
    )

    type_vente = models.CharField(
        max_length=20,
        choices=TYPES_VENTE,
        default='BOUTIQUE'
    )

    date_vente = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='BROUILLON'
    )

    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    frais_livraison = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    zone_livraison = models.ForeignKey(
    "livraisons.ZoneLivraison",
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name="ventes"
)

    def confirmer(self):

        from stock.services import sortir_du_stock

        if self.statut == 'CONFIRMEE':
            return

        if self.statut == 'ANNULEE':
            raise ValueError(
                "Impossible de confirmer une vente annulée."
            )

        if not self.lignes.exists():
            raise ValueError(
                "Impossible de confirmer une vente sans ligne."
            )

        with transaction.atomic():

            # Sortie du stock pour chaque produit vendu
            for ligne in self.lignes.all():

                sortir_du_stock(
                    produit=ligne.produit,
                    quantite=ligne.quantite,
                    motif=f"Vente {self.id}"
                )

            # Calcul du montant total
            total = 0

            for ligne in self.lignes.all():
                total += ligne.quantite * ligne.prix_unitaire

            self.montant_total = total + self.frais_livraison

            self.statut = 'CONFIRMEE'

            self.save()

    def annuler(self):

        if self.statut == "CONFIRMEE":
            raise ValueError(
                "Impossible d'annuler une vente déjà confirmée."
            )

        if self.statut == "ANNULEE":
            return

        self.statut = "ANNULEE"
        self.save()

    def calculer_montant_total(self):

        total = 0

        for ligne in self.lignes.all():
            total += ligne.quantite * ligne.prix_unitaire

        self.montant_total = total + self.frais_livraison

        self.save()


class LigneVente(models.Model):

    vente = models.ForeignKey(
        Vente,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField()

    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.produit.nom} - {self.quantite}"