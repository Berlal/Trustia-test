import re
from decimal import Decimal

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

try:
    from weasyprint import HTML as WeasyHTML
except ImportError:
    WeasyHTML = None

from .forms import FactureForm, FactureLigneFormSet, ProduitForm
from .models import Facture, FactureLigne, Produit

PAGE_SIZE = 10


def _totaux_lignes(lignes):
    return {
        "total_articles": sum(l.quantite for l in lignes),
        "total_ht": sum((l.montant_ht() for l in lignes), Decimal("0")),
        "total_tva": sum((l.montant_tva() for l in lignes), Decimal("0")),
        "total_ttc": sum((l.montant_ttc() for l in lignes), Decimal("0")),
    }


def accueil(request):
    nb_produits = Produit.objects.count()
    nb_produits_catalogue = Produit.objects.filter(actif=True, au_catalogue=True).count()
    nb_factures = Facture.objects.count()
    return render(
        request,
        "catalog/tableau_de_bord.html",
        {
            "nb_produits": nb_produits,
            "nb_produits_catalogue": nb_produits_catalogue,
            "nb_factures": nb_factures,
        },
    )


def produit_liste(request):
    return _produit_liste(request, vue_catalogue=False)


def produit_catalogue(request):
    return _produit_liste(request, vue_catalogue=True)


def _produit_liste(request, *, vue_catalogue: bool):
    params = request.GET.copy()
    if vue_catalogue:
        if "catalogue" not in request.GET:
            params["catalogue"] = "1"
        if "actif" not in request.GET:
            params["actif"] = "1"

    qs = Produit.objects.all()
    q = (params.get("q") or "").strip()
    categorie = (params.get("categorie") or "").strip()
    actif = params.get("actif")
    catalogue = params.get("catalogue")
    if q:
        qs = qs.filter(
            Q(nom__icontains=q)
            | Q(reference_interne__icontains=q)
            | Q(description__icontains=q)
        )
    if categorie:
        qs = qs.filter(categorie__iexact=categorie)
    if actif == "1":
        qs = qs.filter(actif=True)
    elif actif == "0":
        qs = qs.filter(actif=False)
    if catalogue == "1":
        qs = qs.filter(au_catalogue=True)
    elif catalogue == "0":
        qs = qs.filter(au_catalogue=False)
    qs = qs.order_by("nom")
    paginator = Paginator(qs, PAGE_SIZE)
    page = params.get("page") or 1
    produits = paginator.get_page(page)
    categories = (
        Produit.objects.exclude(categorie="")
        .values_list("categorie", flat=True)
        .distinct()
        .order_by("categorie")[:50]
    )
    return render(
        request,
        "catalog/produit_liste.html",
        {
            "produits": produits,
            "q": q,
            "categorie": categorie,
            "actif": actif,
            "catalogue": catalogue,
            "categories": categories,
            "vue_catalogue": vue_catalogue,
        },
    )


def produit_creer(request):
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog:produit_liste")
    else:
        form = ProduitForm()
    return render(request, "catalog/produit_form.html", {"form": form, "titre": "Nouveau produit"})


def produit_modifier(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect("catalog:produit_liste")
    else:
        form = ProduitForm(instance=produit)
    return render(
        request,
        "catalog/produit_form.html",
        {"form": form, "titre": "Modifier le produit", "produit": produit},
    )


def produit_supprimer(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    factures_liees = list(
        Facture.objects.filter(lignes__produit=produit).distinct().order_by("-date_creation")
    )
    peut_supprimer = not factures_liees

    if request.method == "POST":
        if not peut_supprimer:
            messages.error(request, _("Produit encore sur une facture."))
            return redirect("catalog:produit_liste")
        try:
            produit.delete()
        except ProtectedError:
            messages.error(request, _("Référencé par une ligne de facture."))
            return redirect("catalog:produit_liste")
        messages.success(request, _("Produit supprimé."))
        return redirect("catalog:produit_liste")

    return render(
        request,
        "catalog/produit_confirmer_suppression.html",
        {
            "produit": produit,
            "factures_liees": factures_liees,
            "peut_supprimer": peut_supprimer,
        },
    )


def facture_liste(request):
    qs = Facture.objects.all()
    statut = (request.GET.get("statut") or "").strip()
    q = (request.GET.get("q") or "").strip()
    if statut:
        qs = qs.filter(statut=statut)
    if q:
        q_filter = Q(reference__icontains=q) | Q(client_nom__icontains=q) | Q(client_email__icontains=q)
        if q.isdigit():
            q_filter |= Q(pk=int(q))
        qs = qs.filter(q_filter)
    qs = qs.order_by("-date_creation")
    paginator = Paginator(qs, PAGE_SIZE)
    page = request.GET.get("page") or 1
    factures = paginator.get_page(page)
    return render(
        request,
        "catalog/facture_liste.html",
        {
            "factures": factures,
            "statut": statut,
            "q": q,
            "statut_choices": Facture.Statut.choices,
        },
    )


@transaction.atomic
def facture_creer(request):
    if request.method == "POST":
        facture_form = FactureForm(request.POST)
        ligne_formset = FactureLigneFormSet(request.POST, queryset=FactureLigne.objects.none())
        if facture_form.is_valid() and ligne_formset.is_valid():
            facture = facture_form.save()
            for ligne in ligne_formset.save(commit=False):
                ligne.facture = facture
                ligne.save()
            return redirect("catalog:facture_detail", pk=facture.pk)
    else:
        facture_form = FactureForm()
        ligne_formset = FactureLigneFormSet(queryset=FactureLigne.objects.none())
    produits_preview = [
        {"id": p.pk, "nom": p.nom, "prix": str(p.prix), "taux_tva": str(p.taux_tva)}
        for p in Produit.objects.filter(actif=True, au_catalogue=True).order_by("nom")
    ]
    statut_labels = {code: label for code, label in Facture.Statut.choices}
    return render(
        request,
        "catalog/facture_form.html",
        {
            "facture_form": facture_form,
            "ligne_formset": ligne_formset,
            "produits_preview": produits_preview,
            "statut_labels": statut_labels,
        },
    )


def facture_detail(request, pk):
    facture = get_object_or_404(Facture.objects.prefetch_related("lignes__produit"), pk=pk)
    lignes = list(facture.lignes.all())
    tot = _totaux_lignes(lignes)
    return render(
        request,
        "catalog/facture_detail.html",
        {
            "facture": facture,
            "lignes": lignes,
            "nb_lignes": len(lignes),
            **tot,
        },
    )


@require_POST
def facture_maj_theme(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    couleur = (request.POST.get("couleur_theme") or "").strip()
    if not re.match(r"^#[0-9A-Fa-f]{6}$", couleur):
        messages.error(request, _("Couleur invalide (#RRGGBB)."))
        return redirect("catalog:facture_detail", pk=pk)
    facture.couleur_theme = couleur
    facture.save(update_fields=["couleur_theme", "date_modification"])
    messages.success(request, _("Thème enregistré."))
    return redirect("catalog:facture_detail", pk=pk)


def facture_pdf(request, pk):
    facture = get_object_or_404(Facture.objects.prefetch_related("lignes__produit"), pk=pk)
    if WeasyHTML is None:
        messages.error(request, _("PDF indisponible — installer weasyprint."))
        return redirect("catalog:facture_detail", pk=pk)

    couleur = (request.GET.get("couleur") or "").strip()
    if not re.match(r"^#[0-9A-Fa-f]{6}$", couleur):
        couleur = facture.couleur_theme

    lignes = list(facture.lignes.all())
    tot = _totaux_lignes(lignes)
    html_string = render_to_string(
        "catalog/facture_pdf.html",
        {
            "facture": facture,
            "lignes": lignes,
            "couleur_accent": couleur,
            **tot,
        },
        request=request,
    )
    base_url = request.build_absolute_uri("/")
    pdf_bytes = WeasyHTML(string=html_string, base_url=base_url).write_pdf()
    ref = (facture.reference or str(facture.pk)).replace("/", "-")
    filename = f"facture-{ref}.pdf"
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
