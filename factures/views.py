from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.shortcuts import render

from .models import Facture


def imprimer_facture(request, facture_id):

    facture = Facture.objects.get(id=facture_id)

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="facture_{facture.numero}.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    largeur, hauteur = A4

    y = hauteur - 50

    # En-tête entreprise
    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        y,
        "SYLLARAGA"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        "Bio pour bien manger"
    )

    y -= 40


    # Informations facture
    pdf.drawString(
        50,
        y,
        f"Facture N° : {facture.numero}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Date : {facture.date_facture.strftime('%d/%m/%Y')}"
    )

    y -= 30


    # Client
    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Client"
    )

    y -= 20

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"{facture.vente.client.nom} {facture.vente.client.prenom}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Telephone : {facture.vente.client.telephone}"
    )

    y -= 40


    # Produits
    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(50, y, "Produit")
    pdf.drawString(250, y, "Quantite")
    pdf.drawString(330, y, "Prix")
    pdf.drawString(420, y, "Total")

    y -= 20

    pdf.setFont(
        "Helvetica",
        10
    )

    sous_total = 0

    for ligne in facture.vente.lignes.all():

        total_ligne = (
            ligne.quantite *
            ligne.prix_unitaire
        )

        sous_total += total_ligne

        pdf.drawString(
            50,
            y,
            ligne.produit.nom
        )

        pdf.drawString(
            250,
            y,
            str(ligne.quantite)
        )

        pdf.drawString(
            330,
            y,
            str(ligne.prix_unitaire)
        )

        pdf.drawString(
            420,
            y,
            str(total_ligne)
        )

        y -= 20


    y -= 20

    pdf.drawString(
        300,
        y,
        f"Sous-total : {sous_total} FCFA"
    )

    y -= 20

    pdf.drawString(
        300,
        y,
        f"Livraison : {facture.vente.frais_livraison} FCFA"
    )

    y -= 25

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        300,
        y,
        f"TOTAL : {facture.montant_total} FCFA"
    )


    # Paiement
    y -= 40

    pdf.setFont(
        "Helvetica",
        11
    )

    if hasattr(facture.vente, 'paiement'):

        pdf.drawString(
            50,
            y,
            f"Paiement : {facture.vente.paiement.mode_paiement}"
        )


    y -= 40

    pdf.drawString(
        50,
        y,
        "Merci pour votre confiance."
    )


    pdf.save()

    return response
def liste_factures(request):

    factures = Facture.objects.select_related(
        "vente",
        "vente__client"
    ).order_by(
        "-date_facture"
    )

    return render(
        request,
        "factures/liste.html",
        {
            "factures": factures
        }
    )
def detail_facture(request, facture_id):

    facture = Facture.objects.select_related(
        "vente",
        "vente__client"
    ).prefetch_related(
        "vente__lignes__produit"
    ).get(
        id=facture_id
    )

    lignes = facture.vente.lignes.all()

    sous_total = sum(
        ligne.quantite * ligne.prix_unitaire
        for ligne in lignes
    )

    return render(
        request,
        "factures/detail.html",
        {
            "facture": facture,
            "lignes": lignes,
            "sous_total": sous_total
        }
    )        