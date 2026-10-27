from django.db import models,transaction
from django.utils import timezone

from fournisseurs.models import Fournisseur
from produits.models import Produit


class Achat(models.Model):

    STATUTS = (
    ('BROUILLON', 'Brouillon'),
    ('ENVOYE', 'Envoyé au fournisseur'),
    ('COMMANDE', 'Commande validée'),
    ('RECEPTIONNE', 'Réceptionné'),
    ('ANNULE', 'Annulé'),
)

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.CASCADE,
        related_name='achats'
    )

    date_achat = models.DateTimeField(
        auto_now_add=True
    )

    date_reception = models.DateTimeField(
        null=True,
        blank=True
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


    def receptionner(self):

        from stock.models import MouvementStock, LotStock
        from stock.services import generer_numero_lot

        with transaction.atomic():

            if self.statut == "RECEPTIONNE":
                return

            if not self.lignes.exists():
                raise ValueError(
                    "Impossible de réceptionner un achat sans ligne."
                )

            for ligne in self.lignes.all():

                print("CREATION DU LOT POUR :", ligne.produit.nom)

                if (
                    ligne.date_peremption
                    and ligne.date_peremption < timezone.now().date()
                ):
                    raise ValueError(
                        f"Le produit {ligne.produit.nom} possède une date de péremption déjà dépassée."
                    )

                # Création du lot
                lot = LotStock.objects.create(
                    produit=ligne.produit,
                    numero_lot=generer_numero_lot(),
                    quantite=ligne.quantite,
                    prix_achat_unitaire=ligne.prix_unitaire,
                    date_peremption=ligne.date_peremption
                )

                print("LOT CREE :", lot.numero_lot)

                # Historique du mouvement
                MouvementStock.objects.create(
                    produit=ligne.produit,
                    type_mouvement="ENTREE",
                    quantite=ligne.quantite,
                    motif=f"Réception achat fournisseur {self.fournisseur.nom}"
                )

            # Calcul du montant total
            total = 0

            for ligne in self.lignes.all():
                total += ligne.quantite * ligne.prix_unitaire

            self.montant_total = total
            self.statut = "RECEPTIONNE"
            self.date_reception = timezone.now()
            self.save()
    def calculer_montant_total(self):

        total = 0

        for ligne in self.lignes.all():
            total += ligne.quantite * ligne.prix_unitaire

        self.montant_total = total
        self.save()         


    def __str__(self):
        return f"Achat {self.id} - {self.fournisseur.nom}"



class LigneAchat(models.Model):

    achat = models.ForeignKey(
        Achat,
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
    date_peremption = models.DateField(
    null=True,
    blank=True
)


    def __str__(self):
        return f"{self.produit.nom} - {self.quantite}"