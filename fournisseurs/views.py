from django.shortcuts import render, redirect, get_object_or_404

from .forms import FournisseurForm
from .models import Fournisseur


def ajouter_fournisseur(request):

    if request.method == "POST":

        form = FournisseurForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "liste_fournisseurs"
            )

    else:

        form = FournisseurForm()


    return render(
        request,
        "fournisseurs/ajouter.html",
        {
            "form": form
        }
    )



def liste_fournisseurs(request):

    fournisseurs = Fournisseur.objects.all()

    return render(
        request,
        "fournisseurs/liste.html",
        {
            "fournisseurs": fournisseurs
        }
    )



def detail_fournisseur(request, id):

    fournisseur = get_object_or_404(
        Fournisseur,
        id=id
    )

    achats = fournisseur.achats.all()


    return render(
        request,
        "fournisseurs/detail.html",
        {
            "fournisseur": fournisseur,
            "achats": achats
        }
    )