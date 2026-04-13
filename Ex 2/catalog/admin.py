from django.contrib import admin

from .models import Facture, FactureLigne, Produit


class FactureLigneInline(admin.TabularInline):
    model = FactureLigne
    extra = 0
    autocomplete_fields = ("produit",)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "reference_interne",
        "categorie",
        "prix",
        "taux_tva",
        "date_peremption",
        "actif",
        "au_catalogue",
        "cree_le",
    )
    list_filter = ("actif", "au_catalogue", "categorie")
    search_fields = ("nom", "reference_interne", "description", "categorie")
    ordering = ("nom",)


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ("id", "reference", "statut", "client_nom", "devise", "date_creation")
    list_filter = ("statut", "devise")
    search_fields = ("reference", "client_nom", "client_email", "notes_internes")
    inlines = [FactureLigneInline]
    readonly_fields = ("date_creation", "date_modification")


@admin.register(FactureLigne)
class FactureLigneAdmin(admin.ModelAdmin):
    list_display = ("facture", "produit", "quantite", "remise_pourcent")
    autocomplete_fields = ("facture", "produit")
