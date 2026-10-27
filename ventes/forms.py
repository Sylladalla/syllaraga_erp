from django import forms
from .models import Vente, LigneVente


class VenteForm(forms.ModelForm):

    class Meta:

        model = Vente

        fields = [
            "client",
            "type_vente",
            "frais_livraison",
        ]

        widgets = {

            "client": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "type_vente": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "frais_livraison": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01"
                }
            ),

        }
class LigneVenteForm(forms.ModelForm):

    class Meta:

        model = LigneVente

        fields = [
            "produit",
            "quantite",
            "prix_unitaire",
        ]

        widgets = {

            "produit": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "quantite": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),

            "prix_unitaire": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
        }        