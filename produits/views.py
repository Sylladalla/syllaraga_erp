from django.shortcuts import render, redirect

from .models import Produit, Categorie
from .forms import ProduitForm, CategorieForm


def liste_produits(request):

    produits = Produit.objects.all().order_by("-date_creation")

    return render(
        request,
        "produits/liste.html",
        {
            "produits": produits
        }
    )


def ajouter_produit(request):

    if request.method == "POST":

        form = ProduitForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("liste_produits")

    else:

        form = ProduitForm()

    return render(
        request,
        "produits/formulaire.html",
        {
            "form": form,
            "titre": "Ajouter un produit"
        }
    )


def liste_categories(request):

    categories = Categorie.objects.all()

    return render(
        request,
        "produits/liste_categories.html",
        {
            "categories": categories
        }
    )


def ajouter_categorie(request):

    if request.method == "POST":

        form = CategorieForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("liste_categories")

    else:

        form = CategorieForm()

    return render(
        request,
        "produits/categories.html",
        {
            "form": form,
            "titre": "Ajouter une catégorie"
        }
    )
from django.shortcuts import get_object_or_404


def modifier_produit(request, id):

    produit = get_object_or_404(
        Produit,
        id=id
    )

    if request.method == "POST":

        form = ProduitForm(
            request.POST,
            instance=produit
        )

        if form.is_valid():

            form.save()

            return redirect("liste_produits")

    else:

        form = ProduitForm(
            instance=produit
        )

    return render(
        request,
        "produits/formulaire.html",
        {
            "form": form,
            "titre": "Modifier un produit"
        }
    )  
def supprimer_produit(request, id):

    produit = get_object_or_404(
        Produit,
        id=id
    )


    if request.method == "POST":

        produit.delete()

        return redirect("liste_produits")


    return render(
        request,
        "produits/confirmer_suppression.html",
        {
            "produit": produit
        }
    )      
    from .models import Produit, Categorie
def liste_categories(request):

    categories = Categorie.objects.all()

    return render(
        request,
        "produits/liste_categories.html",
        {
            "categories": categories
        }
    )
def ajouter_categorie(request):

    if request.method == "POST":

        form = CategorieForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("liste_categories")

    else:

        form = CategorieForm()


    return render(
        request,
        "produits/categories.html",
        {
            "form": form,
            "titre": "Ajouter une catégorie"
        }
    )   
def modifier_categorie(request, id):

    categorie = get_object_or_404(
        Categorie,
        id=id
    )


    if request.method == "POST":

        form = CategorieForm(
            request.POST,
            instance=categorie
        )


        if form.is_valid():

            form.save()

            return redirect("liste_categories")


    else:

        form = CategorieForm(
            instance=categorie
        )


    return render(
        request,
        "produits/categories.html",
        {
            "form": form,
            "titre": "Modifier une catégorie"
        }
    )  
def supprimer_categorie(request, id):

    categorie = get_object_or_404(
        Categorie,
        id=id
    )


    if request.method == "POST":

        categorie.delete()

        return redirect("liste_categories")


    return render(
        request,
        "produits/confirmer_suppression_categorie.html",
        {
            "categorie": categorie
        }
    )           