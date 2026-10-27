

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import (
    InscriptionClientForm,
    ConnexionClientForm,
    MotDePasseOublieForm,
    ReinitialiserMotDePasseForm,
)
from .models import Client

def inscription_client(request):
    if request.method == "POST":
        form = InscriptionClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)

            client.mot_de_passe = make_password(
                form.cleaned_data["mot_de_passe"]
            )

            client.save()

            messages.success(
                request,
                "Votre compte a été créé. Vous pouvez vous connecter.",
            )

            return redirect("connexion_client")

    else:
        form = InscriptionClientForm()

    return render(
        request,
        "clients/inscription.html",
        {"form": form},
    )



def connexion_client(request):
    if request.method == "POST":
        form = ConnexionClientForm(request.POST)

        if form.is_valid():
            telephone = form.cleaned_data["telephone"].strip()
            mot_de_passe = form.cleaned_data["mot_de_passe"]

            client = Client.objects.filter(
                telephone=telephone
            ).first()

            if client and check_password(
                mot_de_passe,
                client.mot_de_passe,
            ):
                request.session["client_id"] = client.pk
                request.session["client_nom"] = (
                    f"{client.prenom} {client.nom}"
                )

                messages.success(
                    request,
                    f"Bienvenue {client.prenom} !",
                )

                destination = request.GET.get("next")

                if destination and url_has_allowed_host_and_scheme(
                    destination,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(destination)

                return redirect("mes_commandes")

            messages.error(
                request,
                "Téléphone ou mot de passe incorrect.",
            )
    else:
        form = ConnexionClientForm()

    return render(
        request,
        "clients/connexion.html",
        {"form": form},
    )



def accueil_clients(request):
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("connexion_client")

    client = Client.objects.filter(pk=client_id).first()

    if not client:
        request.session.flush()
        return redirect("connexion_client")

    return render(
        request,
        "clients/accueil.html",
        {"client": client},
    )


def deconnexion_client(request):
    request.session.pop("client_id", None)
    request.session.pop("client_nom", None)

    messages.success(request, "Vous êtes déconnecté.")
    return redirect("connexion_client")


def mot_de_passe_oublie(request):
    if request.method == "POST":
        form = MotDePasseOublieForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()

            client = Client.objects.filter(
                email__iexact=email
            ).first()

            # Même réponse si l'adresse n'existe pas.
            # Cela évite de révéler les comptes enregistrés.
            if client:
                token = client.generer_token_reinitialisation()

                lien = request.build_absolute_uri(
                    reverse(
                        "reinitialiser_mot_de_passe",
                        kwargs={"token": token},
                    )
                )

                try:
                    send_mail(
                        subject="Réinitialisation du mot de passe Syllaraga",
                        message=(
                            "Bonjour,\n\n"
                            "Pour choisir un nouveau mot de passe, "
                            "ouvrez ce lien valable pendant une heure :\n\n"
                            f"{lien}\n\n"
                            "Si vous n'avez pas demandé cette opération, "
                            "ignorez ce message."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                except Exception:
                    # Le message reste générique côté utilisateur.
                    # L'erreur technique sera visible dans le terminal.
                    import logging
                    logging.getLogger(__name__).exception(
                        "Échec de l'envoi de l'e-mail de réinitialisation."
                    )

            messages.success(
                request,
                "Si cette adresse correspond à un compte, "
                "un lien de réinitialisation sera envoyé.",
            )
            return redirect("mot_de_passe_oublie")
    else:
        form = MotDePasseOublieForm()

    return render(
        request,
        "clients/mot_de_passe_oublie.html",
        {"form": form},
    )


def reinitialiser_mot_de_passe(request, token):
    client = Client.objects.filter(
        token_reinitialisation=token
    ).first()

    if (
        not client
        or not client.token_expiration
        or client.token_expiration <= timezone.now()
    ):
        messages.error(
            request,
            "Ce lien est invalide ou a expiré. "
            "Demandez une nouvelle réinitialisation.",
        )
        return redirect("mot_de_passe_oublie")

    if request.method == "POST":
        form = ReinitialiserMotDePasseForm(request.POST)

        if form.is_valid():
            client.mot_de_passe = make_password(
                form.cleaned_data["mot_de_passe"]
            )
            client.token_reinitialisation = None
            client.token_expiration = None
            client.save(
                update_fields=[
                    "mot_de_passe",
                    "token_reinitialisation",
                    "token_expiration",
                ]
            )

            messages.success(
                request,
                "Votre mot de passe a été modifié. "
                "Vous pouvez maintenant vous connecter.",
            )
            return redirect("connexion_client")
    else:
        form = ReinitialiserMotDePasseForm()

    return render(
        request,
        "clients/reinitialiser_mot_de_passe.html",
        {"form": form},
    )
