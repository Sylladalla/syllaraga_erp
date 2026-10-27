from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Transformation,  LigneTransformation
from .forms import (
    ProduitFinalForm,
    TransformationForm,
    LigneTransformationForm
)
def liste_transformations(request):

    transformations = Transformation.objects.all().order_by(
        "-date_transformation"
    )

    return render(
        request,
        "transformations/liste.html",
        {
            "transformations": transformations
        }
    )

def creer_transformation(request):

    LigneFormSet = inlineformset_factory(
        Transformation,
        LigneTransformation,
        form=LigneTransformationForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":

        produit_form = ProduitFinalForm(
            request.POST,
            request.FILES
        )

        form = TransformationForm(
            request.POST
        )

        formset = LigneFormSet(
            request.POST,
            prefix="lignes"
        )

        if (
            produit_form.is_valid()
            and form.is_valid()
            and formset.is_valid()
        ):

            produit = produit_form.save()

            transformation = form.save(
                commit=False
            )

            transformation.produit = produit
            transformation.save()

            formset.instance = transformation
            formset.save()

            messages.success(
                request,
                "La transformation a été créée avec succès."
            )

            return redirect(
                "detail_transformation",
                transformation.id
            )

    else:

        produit_form = ProduitFinalForm()

        form = TransformationForm()

        formset = LigneFormSet(
            prefix="lignes"
        )

    return render(
        request,
        "transformations/formulaire.html",
        {
            "produit_form": produit_form,
            "form": form,
            "formset": formset
        }
    )

def detail_transformation(request, id):

    transformation = get_object_or_404(
        Transformation,
        id=id
    )

    return render(
        request,
        "transformations/detail.html",
        {
            "transformation": transformation
        }
    )


def terminer_transformation(request, id):

    transformation = get_object_or_404(
        Transformation,
        id=id
    )

    if transformation.statut == "TERMINEE":

        messages.warning(
            request,
            "Cette transformation est déjà terminée."
        )

    elif transformation.statut == "ANNULEE":

        messages.error(
            request,
            "Une transformation annulée ne peut pas être terminée."
        )

    else:

        try:

            transformation.terminer()

            messages.success(
                request,
                "La transformation a été terminée avec succès."
            )

        except ValueError as e:

            messages.error(
                request,
                str(e)
            )

    return redirect(
        "detail_transformation",
        transformation.id
    )


def annuler_transformation(request, id):

    transformation = get_object_or_404(
        Transformation,
        id=id
    )

    if transformation.statut == "TERMINEE":

        messages.error(
            request,
            "Une transformation déjà terminée ne peut pas être annulée."
        )

    elif transformation.statut == "ANNULEE":

        messages.warning(
            request,
            "Cette transformation est déjà annulée."
        )

    else:

        transformation.statut = "ANNULEE"

        transformation.save()

        messages.success(
            request,
            "La transformation a été annulée."
        )

    return redirect(
        "detail_transformation",
        transformation.id
    )