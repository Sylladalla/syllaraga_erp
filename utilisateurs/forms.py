from django import forms
from .models import Utilisateur


class UtilisateurCreationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Utilisateur

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "role",
            "password",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "telephone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }

    def save(self, commit=True):
        utilisateur = super().save(commit=False)

        utilisateur.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            utilisateur.save()

        return utilisateur