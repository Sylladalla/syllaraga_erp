
from django import forms
from .models import Livraison, ZoneLivraison


class LivraisonForm(forms.ModelForm):

    class Meta:
        model = Livraison

        fields = [
            "adresse_livraison",
            "zone",
            "livreur",
            "telephone_livreur",
            "statut",
        ]

        widgets = {

            "adresse_livraison": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "zone": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "livreur": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "telephone_livreur": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "statut": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }


class ZoneLivraisonForm(forms.ModelForm):

    class Meta:
        model = ZoneLivraison

        fields = [
            "nom",
            "frais",
        ]

        widgets = {

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Bamako-Centre"
                }
            ),

            "frais": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : 1500"
                }
            ),
        }