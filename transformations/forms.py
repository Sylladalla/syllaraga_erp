
from django import forms

from .models import Transformation, LigneTransformation
from produits.models import Produit


class ProduitFinalForm(forms.ModelForm):

    class Meta:
        model = Produit

        fields = [
            "nom",
            "categorie",
            "image",
            "prix_achat",
            "prix_vente",
            "unite_mesure",
            "est_perissable",
        ]

        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Jus d'ananas"
                }
            ),

            "categorie": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),

            "prix_achat": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01"
                }
            ),

            "prix_vente": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01"
                }
            ),

            "unite_mesure": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : bouteille"
                }
            ),

            "est_perissable": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def save(self, commit=True):

        produit = super().save(commit=False)

        produit.type_produit = "PRODUIT_TRANSFORME"

        if commit:
            produit.save()

        return produit


class TransformationForm(forms.ModelForm):

    class Meta:
        model = Transformation

        fields = [
            "quantite_produite",
            "date_peremption",
        ]

        widgets = {
            "quantite_produite": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "date_peremption": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }


class LigneTransformationForm(forms.ModelForm):

    class Meta:
        model = LigneTransformation

        fields = [
            "produit",
            "quantite_utilisee",
        ]

        widgets = {
            "produit": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "quantite_utilisee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["produit"].queryset = Produit.objects.filter(
    type_produit__in=[
        "MATIERE_PREMIERE",
        "INGREDIENT",
        "EMBALLAGE",
    ]
)