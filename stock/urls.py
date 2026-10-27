from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.liste_stock,
        name="liste_stock"
    ),

    path(
        "lots/",
        views.liste_lots,
        name="liste_lots"
    ),

    path(
        "<int:id>/",
        views.detail_stock,
        name="detail_stock"
    ),

    path(
        "alertes/",
        views.alertes_peremption,
        name="alertes_peremption"
    ),
    path(
    "faibles/",
    views.stocks_faibles_view,
    name="stocks_faibles"
),
path(
    "perimes/",
    views.lots_perimes_view,
    name="lots_perimes"
),
path(
    "ruptures/",
    views.ruptures_stock_view,
    name="liste_ruptures"
),
]