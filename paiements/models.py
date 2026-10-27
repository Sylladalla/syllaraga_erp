
from django.db import models, transaction
from achats.models import Achat
from ventes.models import Vente


class Paiement(models.Model):

    MODES_PAIEMENT = (
        ('ESPECES', 'Espèces'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('MOOV_MONEY', 'Moov Money'),
        ('CARTE', 'Visa / Mastercard'),
    )

    STATUTS = (
        ('EN_ATTENTE', 'En attente'),
        ('PAYE', 'Payé'),
        ('ECHEC', 'Échec'),
    )

    vente = models.OneToOneField(
        Vente,
        on_delete=models.CASCADE,
        related_name='paiement'
    )

    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    mode_paiement = models.CharField(
        max_length=20,
        choices=MODES_PAIEMENT
    )

    reference_cinetpay = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='EN_ATTENTE'
    )

    date_paiement = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        self.montant = self.vente.montant_total

        super().save(*args, **kwargs)

    def effectuer(self):

        if self.statut == 'PAYE':
            return

        if self.statut == 'ECHEC':
            raise ValueError(
                "Impossible d'effectuer un paiement en échec."
            )

        with transaction.atomic():

            # La vente doit être confirmée après
            # la validation réelle du paiement.
            self.vente.confirmer()

            # Le paiement est marqué comme payé
            # seulement si la confirmation de la vente
            # s'est correctement déroulée.
            self.statut = 'PAYE'
            self.save()

            # Création de la facture après paiement
                        # Création de la facture après paiement
            from factures.models import Facture

            Facture.objects.get_or_create(
                vente=self.vente
            )

            # Création de la livraison pour une vente en ligne
            if self.vente.type_vente == "EN_LIGNE":

                from livraisons.models import Livraison

                Livraison.objects.get_or_create(
                    vente=self.vente,
                    defaults={
                        "adresse_livraison": self.vente.client.adresse,
                        "zone": self.vente.zone_livraison,
                        "statut": "EN_PREPARATION",
                    }
                )

    def __str__(self):

        return f"Paiement {self.vente.id}"

    
class PaiementFournisseur(models.Model):

    MODES_PAIEMENT = (
        ("ESPECES", "Espèces"),
        ("VIREMENT", "Virement bancaire"),
        ("ORANGE_MONEY", "Orange Money"),
        ("MOOV_MONEY", "Moov Money"),
    )

    achat = models.ForeignKey(
        Achat,
        on_delete=models.PROTECT,
        related_name="paiements_fournisseur",
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    mode_paiement = models.CharField(
        max_length=20,
        choices=MODES_PAIEMENT,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    date_paiement = models.DateTimeField(
        auto_now_add=True,
    )

    observation = models.TextField(blank=True)

    def __str__(self):
        return (
            f"Paiement fournisseur - "
            f"Achat {self.achat_id} - {self.montant}"
        )
