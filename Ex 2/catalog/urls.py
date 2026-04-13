from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("catalogue/", views.produit_catalogue, name="catalogue"),
    path("produits/", views.produit_liste, name="produit_liste"),
    path("produits/nouveau/", views.produit_creer, name="produit_creer"),
    path("produits/<int:pk>/modifier/", views.produit_modifier, name="produit_modifier"),
    path("produits/<int:pk>/supprimer/", views.produit_supprimer, name="produit_supprimer"),
    path("factures/", views.facture_liste, name="facture_liste"),
    path("factures/nouvelle/", views.facture_creer, name="facture_creer"),
    path("factures/<int:pk>/", views.facture_detail, name="facture_detail"),
    path("factures/<int:pk>/pdf/", views.facture_pdf, name="facture_pdf"),
    path("factures/<int:pk>/theme/", views.facture_maj_theme, name="facture_maj_theme"),
]
