
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from utilisateurs.decorators import role_requis
from .services import stocks_faibles, lots_perimes
from .models import Stock, LotStock

@role_requis(roles=['ADMINISTRATEUR', 'MAGASINIER'])
def liste_stock(request):


    recherche = request.GET.get("recherche")

    stocks = Stock.objects.select_related(
    "produit"
).order_by(
    "-produit__date_creation"
)

    if recherche:
        stocks = stocks.filter(
            Q(produit__nom__icontains=recherche)
        )

    stocks_faibles_liste = stocks_faibles()

    paginator = Paginator(
        stocks,
        10
    )

    page = request.GET.get("page")

    stocks = paginator.get_page(page)

    return render(
        request,
        "stock/liste.html",
        {
            "stocks": stocks,
            "recherche": recherche,
            "stocks_faibles": stocks_faibles_liste,
        }
    )

@role_requis(["ADMIN", "STOCK", "MAGASINIER"])
def detail_stock(request, id):
    stock = get_object_or_404(
        Stock,
        id=id
    )

    lots = stock.produit.lots.all().order_by(
        "date_peremption"
    )

    mouvements = stock.produit.mouvements_stock.all().order_by(
        "-date_mouvement"
    )

    aujourd_hui = timezone.now().date()

    limite = aujourd_hui + timedelta(days=7)

    lots_alertes = lots.filter(
        date_peremption__lte=limite,
        date_peremption__isnull=False,
        quantite__gt=0
    )

    return render(
        request,
        "stock/detail.html",
        {
            "stock": stock,
            "lots": lots,
            "mouvements": mouvements,
            "lots_alertes": lots_alertes,
            "today": aujourd_hui,
            "limite": limite,
        }
    )


def alertes_peremption(request):

    aujourd_hui = timezone.now().date()

    limite = aujourd_hui + timedelta(days=7)

    lots_alertes = LotStock.objects.filter(
        date_peremption__gte=aujourd_hui,
        date_peremption__lte=limite,
        quantite__gt=0
    ).order_by(
        "date_peremption"
    )

    return render(
        request,
        "stock/alertes.html",
        {
            "lots_alertes": lots_alertes,
            "today": aujourd_hui,
            "limite": limite,
        }
    )
def liste_lots(request):

    aujourd_hui = timezone.now().date()

    limite = aujourd_hui + timedelta(days=7)

    lots = LotStock.objects.select_related(
        "produit"
    ).order_by(
        "date_peremption"
    )

    return render(
        request,
        "stock/lots.html",
        {
            "lots": lots,
            "today": aujourd_hui,
            "limite": limite,
        }
    )  
def stocks_faibles_view(request):

    stocks = stocks_faibles().select_related(
        "produit"
    ).order_by(
        "quantite_disponible"
    )

    return render(
        request,
        "stock/faibles.html",
        {
            "stocks": stocks
        }
    ) 
def lots_perimes_view(request):

    lots = lots_perimes()

    return render(
        request,
        "stock/perimes.html",
        {
            "lots": lots
        }
    )
def ruptures_stock_view(request):

    stocks = Stock.objects.filter(
        quantite_disponible=0
    ).select_related(
        "produit"
    ).order_by(
        "produit__nom"
    )

    return render(
        request,
        "stock/ruptures.html",
        {
            "stocks": stocks
        }
    )           