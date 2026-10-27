

from django import forms
from django.forms import inlineformset_factory

from .models import Achat, LigneAchat


class AchatForm(forms.ModelForm):

    class Meta:
        model = Achat
        fields = ["fournisseur"]

        widgets = {
            "fournisseur": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class LigneAchatForm(forms.ModelForm):

    class Meta:
        model = LigneAchat
        fields = [
            "produit",
            "quantite",
            "prix_unitaire",
            "date_peremption",
        ]

        widgets = {
            "produit": forms.Select(
                attrs={"class": "form-select"}
            ),
            "quantite": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "prix_unitaire": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "step": "0.01"}
            ),
            "date_peremption": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


LigneAchatFormSet = inlineformset_factory(
    Achat,
    LigneAchat,
    form=LigneAchatForm,
    extra=1,
    can_delete=True
)
