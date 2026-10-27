#from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):

    TYPES_PRODUIT = (
        ('MATIERE_PREMIERE', 'Matière première'),
        ('INGREDIENT', 'Ingrédient'),
        ('EMBALLAGE', 'Emballage'),
        ('PRODUIT_ACHETE', 'Produit acheté'),
        ('PRODUIT_TRANSFORME', 'Produit transformé'),
    )

    nom = models.CharField(
    max_length=100,
    unique=True
)
    description = models.TextField(blank=True, null=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produits'
    )
    image = models.ImageField(
    upload_to="produits/",
    blank=True,
    null=True
)

    type_produit = models.CharField(
        max_length=30,
        choices=TYPES_PRODUIT
    )

    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unite_mesure = models.CharField(
        max_length=50
    )

    # date_expiration = models.DateField(
    #     blank=True,
    #     null=True
    # )

    est_perissable = models.BooleanField(
        default=True
    )
    date_creation = models.DateTimeField(
    auto_now_add=True
)

    def __str__(self):
        return self.nom