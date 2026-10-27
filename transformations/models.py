
from django.db import models
from produits.models import Produit


class Transformation(models.Model):

    STATUTS = (
        ('BROUILLON', 'Brouillon'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='transformations'
    )

    quantite_produite = models.PositiveIntegerField()
    cout_total = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0
)

    cout_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    date_peremption = models.DateField(
        blank=True,
        null=True
    )

    date_transformation = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='BROUILLON'
    )

    def terminer(self):

        from django.db import transaction
        from stock.services import (
            sortir_du_stock,
            generer_numero_lot
        )
        from stock.models import (
            LotStock,
            MouvementStock
        )

        if self.statut == 'TERMINEE':
            return

        with transaction.atomic():

            # Vérifier que le produit final est transformé
            if self.produit.type_produit != 'PRODUIT_TRANSFORME':
                raise ValueError(
                    "Le produit final doit être un produit transformé."
                )

            # Vérifier la date de péremption
            if (
                self.produit.est_perissable
                and not self.date_peremption
            ):
                raise ValueError(
                    "Une date de péremption est obligatoire "
                    "pour un produit périssable."
                )
            # Calcul du coût total de la transformation
            cout_total = 0

            for ligne in self.lignes.all():

                cout_total += (
                    ligne.quantite_utilisee
                    * ligne.produit.prix_achat
                )

                # Calcul du coût unitaire
                cout_unitaire = (
                    cout_total / self.quantite_produite
                )

                self.cout_total = cout_total
                self.cout_unitaire = cout_unitaire
                self.save()       
            # Calcul du coût total de la transformation
            cout_total = 0

            for ligne in self.lignes.all():

                cout_total += (
                    ligne.quantite_utilisee
                    * ligne.produit.prix_achat
                )

            # Calcul du coût unitaire
            cout_unitaire = (
                cout_total / self.quantite_produite
            )

            self.cout_total = cout_total
            self.cout_unitaire = cout_unitaire
            self.save()

            # Sortie des matières premières
            for ligne in self.lignes.all():

                sortir_du_stock(
                    produit=ligne.produit,
                    quantite=ligne.quantite_utilisee,
                    motif=f"Transformation {self.id}"
                )

            # Création du lot du produit final
            LotStock.objects.create(
                produit=self.produit,
                numero_lot=generer_numero_lot(),
                quantite=self.quantite_produite,
                prix_achat_unitaire=self.produit.prix_achat,
                date_peremption=self.date_peremption
            )

            # Entrée dans le stock
            MouvementStock.objects.create(
                produit=self.produit,
                type_mouvement='ENTREE',
                quantite=self.quantite_produite,
                motif=f"Production transformation {self.id}"
            )

            # Transformation terminée
            self.statut = 'TERMINEE'
            self.save()

    def __str__(self):
        return (
            f"{self.produit.nom} - "
            f"{self.quantite_produite}"
        )


class LigneTransformation(models.Model):

    transformation = models.ForeignKey(
        Transformation,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite_utilisee = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"{self.produit.nom} - "
            f"{self.quantite_utilisee}"
        )