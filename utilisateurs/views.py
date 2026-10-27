
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UtilisateurCreationForm
from .models import Utilisateur
from django.contrib.auth import authenticate, login, logout
from .decorators import role_requis
@role_requis(["ADMIN"])
def liste_utilisateurs(request):

    utilisateurs = Utilisateur.objects.all().order_by(
        "username"
    )

    return render(
        request,
        "utilisateurs/liste.html",
        {
            "utilisateurs": utilisateurs
        }
    )

@role_requis(["ADMIN"])
def creer_utilisateur(request):

    if request.method == "POST":

        form = UtilisateurCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "L'utilisateur a été créé avec succès."
            )

            return redirect(
                "liste_utilisateurs"
            )

    else:

        form = UtilisateurCreationForm()

    return render(
        request,
        "utilisateurs/formulaire.html",
        {
            "form": form
        }
    )

def redirection_selon_role(utilisateur):
    """Dirige chaque employé vers une page correspondant à son rôle."""

    destinations = {
        "ADMIN": "dashboard",
        "STOCK": "liste_stock",
        "MAGASINIER": "liste_stock",
        "VENDEUR": "liste_ventes",
        "LIVREUR": "liste_livraisons",
        "EMPLOYE": "accueil",
    }

    destination = destinations.get(
        utilisateur.role,
        "accueil"
    )

    return redirect(destination)


def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        utilisateur = authenticate(
            request,
            username=username,
            password=password
        )

        if utilisateur is not None:
            login(request, utilisateur)

            messages.success(
                request,
                f"Bienvenue {utilisateur.username}."
            )


            return redirection_selon_role(utilisateur)

        messages.error(
            request,
            "Nom d'utilisateur ou mot de passe incorrect."
        )

    return render(request, "utilisateurs/connexion.html")


def deconnexion(request):

    logout(request)

    messages.success(
        request,
        "Vous êtes déconnecté."
    )

    return redirect("connexion")    
# Tout en bas de utilisateurs/views.py
@role_requis(roles=['ADMINISTRATEUR', 'VENDEUR', 'MAGASINIER', 'LIVREUR']) # Tout le monde a le droit de voir le dashboard
def dashboard(request):
    return render(request, "utilisateurs/dashboard.html")

