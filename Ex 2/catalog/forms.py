import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet, modelformset_factory

from .models import Facture, FactureLigne, Produit


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            "nom",
            "reference_interne",
            "description",
            "categorie",
            "prix",
            "taux_tva",
            "date_peremption",
            "actif",
            "au_catalogue",
        ]
        labels = {
            "nom": "Nom",
            "reference_interne": "Réf. / SKU",
            "description": "Description",
            "categorie": "Catégorie",
            "prix": "Prix HT (€)",
            "taux_tva": "TVA (%)",
            "date_peremption": "Péremption",
            "actif": "Actif",
            "au_catalogue": "Au catalogue",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = [
            "reference",
            "statut",
            "client_nom",
            "client_email",
            "client_telephone",
            "adresse_facturation",
            "devise",
            "notes_internes",
            "couleur_theme",
        ]
        labels = {
            "reference": "Réf. facture",
            "statut": "Statut",
            "client_nom": "Client",
            "client_email": "E-mail",
            "client_telephone": "Tél.",
            "adresse_facturation": "Adresse",
            "devise": "Devise",
            "notes_internes": "Notes internes",
            "couleur_theme": "Thème (#RGB)",
        }
        widgets = {
            "adresse_facturation": forms.Textarea(attrs={"rows": 3}),
            "notes_internes": forms.Textarea(attrs={"rows": 2}),
            "couleur_theme": forms.HiddenInput(attrs={"id": "facture-theme-couleur"}),
        }

    def clean_couleur_theme(self):
        raw = (self.cleaned_data.get("couleur_theme") or "").strip() or "#1a73e8"
        if not re.match(r"^#[0-9A-Fa-f]{6}$", raw):
            raise ValidationError("#RRGGBB attendu.")
        return raw


class FactureLigneForm(forms.ModelForm):
    class Meta:
        model = FactureLigne
        fields = ["produit", "quantite", "remise_pourcent", "libelle_override"]
        labels = {
            "produit": "Produit",
            "quantite": "Qté",
            "remise_pourcent": "Remise %",
            "libelle_override": "Libellé (opt.)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ("produit", "quantite", "remise_pourcent", "libelle_override"):
            self.fields[f].required = False
        self.fields["produit"].queryset = Produit.objects.filter(
            actif=True, au_catalogue=True
        ).order_by("nom")

    def clean(self):
        cleaned = super().clean()
        produit = cleaned.get("produit")
        quantite = cleaned.get("quantite")
        if produit and not quantite:
            raise forms.ValidationError("Quantité requise si produit.")
        if quantite and not produit:
            raise forms.ValidationError("Produit requis si quantité.")
        return cleaned


class BaseFactureLigneFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        ok = 0
        for form in self.forms:
            cd = getattr(form, "cleaned_data", None)
            if not cd:
                continue
            p, q = cd.get("produit"), cd.get("quantite")
            if p and q:
                ok += 1
            elif p or q:
                raise forms.ValidationError("Ligne incomplète (produit + qté).")
        if ok < 1:
            raise forms.ValidationError("Au moins une ligne complète.")
        seen = set()
        for form in self.forms:
            cd = getattr(form, "cleaned_data", None)
            if not cd:
                continue
            p = cd.get("produit")
            if p:
                if p.pk in seen:
                    raise forms.ValidationError("Produit en double.")
                seen.add(p.pk)


FactureLigneFormSet = modelformset_factory(
    FactureLigne,
    form=FactureLigneForm,
    formset=BaseFactureLigneFormSet,
    extra=4,
    min_num=0,
    can_delete=False,
)
