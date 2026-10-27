

from django import forms

from .models import Paiement, PaiementFournisseur


class PaiementForm(forms.ModelForm):

    class Meta:
        model = Paiement
        fields = ["mode_paiement"]

        widgets = {
            "mode_paiement": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class PaiementFournisseurForm(forms.ModelForm):

    class Meta:
        model = PaiementFournisseur

        fields = [
            "montant",
            "mode_paiement",
            "reference",
            "observation",
        ]

        widgets = {
            "montant": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "Montant à payer",
                }
            ),
            "mode_paiement": forms.Select(
                attrs={"class": "form-select"}
            ),
            "reference": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Référence du paiement (facultatif)",
                }
            ),
            "observation": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observation (facultatif)",
                }
            ),
        }

    def clean_montant(self):
        montant = self.cleaned_data["montant"]

        if montant <= 0:
            raise forms.ValidationError(
                "Le montant doit être supérieur à zéro."
            )

        return montant
