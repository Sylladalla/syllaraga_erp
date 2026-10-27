

from django import forms

from .models import Client


class InscriptionClientForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=8,
    )

    confirmation = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Client
        fields = [
            "nom",
            "prenom",
            "telephone",
            "email",
            "adresse",
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "adresse": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def clean_telephone(self):
        telephone = self.cleaned_data["telephone"].strip()
        if Client.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError(
                "Ce numéro de téléphone est déjà utilisé."
            )
        return telephone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.strip().lower()
            if Client.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError(
                    "Cette adresse e-mail est déjà utilisée."
                )
        return email

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("confirmation")

        if mot_de_passe and confirmation and mot_de_passe != confirmation:
            self.add_error(
                "confirmation",
                "Les deux mots de passe ne correspondent pas.",
            )

        return cleaned_data


class ConnexionClientForm(forms.Form):
    telephone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class MotDePasseOublieForm(forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )


class ReinitialiserMotDePasseForm(forms.Form):
    mot_de_passe = forms.CharField(
        label="Nouveau mot de passe",
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    confirmation = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("confirmation")

        if mot_de_passe and confirmation and mot_de_passe != confirmation:
            self.add_error(
                "confirmation",
                "Les deux mots de passe ne correspondent pas.",
            )

        return cleaned_data
