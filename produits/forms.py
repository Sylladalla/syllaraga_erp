from django import forms

from .models import Produit, Categorie



class ProduitForm(forms.ModelForm):

    class Meta:

        model = Produit

        fields = "__all__"

        widgets = {

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "categorie": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "type_produit": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "prix_achat": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "prix_vente": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "unite_mesure": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }



class CategorieForm(forms.ModelForm):

    class Meta:

        model = Categorie

        fields = [
            "nom",
            "description"
        ]

        widgets = {

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

        }