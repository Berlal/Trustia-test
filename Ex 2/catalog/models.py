from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    reference_interne = models.CharField(max_length=64, blank=True, db_index=True, help_text="SKU")
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=64, blank=True, db_index=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_peremption = models.DateField("date de péremption")
    actif = models.BooleanField(default=True, db_index=True)
    au_catalogue = models.BooleanField("au catalogue", default=True, db_index=True, help_text="Liste + factures")
    taux_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("20.00"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
        help_text="TVA %",
    )
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom"]
        indexes = [
            models.Index(fields=["actif", "nom"]),
            models.Index(fields=["actif", "au_catalogue"], name="catalog_pro_actif_auc_idx"),
        ]

    def __str__(self) -> str:
        return self.nom


class Facture(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        ENVOYEE = "envoyee", "Envoyée"
        PAYEE = "payee", "Payée"
        ANNULEE = "annulee", "Annulée"

    reference = models.CharField(max_length=64, blank=True, db_index=True)
    statut = models.CharField(max_length=16, choices=Statut.choices, default=Statut.BROUILLON, db_index=True)
    client_nom = models.CharField("client / raison sociale", max_length=255, blank=True)
    client_email = models.EmailField(blank=True)
    client_telephone = models.CharField(max_length=32, blank=True)
    adresse_facturation = models.TextField(blank=True)
    devise = models.CharField(max_length=3, default="EUR")
    notes_internes = models.TextField(blank=True, help_text="Interne")
    couleur_theme = models.CharField(
        max_length=7,
        default="#1a73e8",
        help_text="#RGB aperçu/PDF",
        validators=[
            RegexValidator(regex=r"^#[0-9A-Fa-f]{6}$", message="#RRGGBB"),
        ],
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]
        indexes = [models.Index(fields=["statut", "-date_creation"])]

    def __str__(self) -> str:
        if self.reference:
            return self.reference
        return f"Facture #{self.pk}"


class FactureLigne(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    remise_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
        help_text="Remise %",
    )
    libelle_override = models.CharField(max_length=255, blank=True, help_text="Surcharge libellé")

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(fields=["facture", "produit"], name="unique_produit_par_facture")
        ]

    def libelle_facture(self) -> str:
        return self.libelle_override.strip() if self.libelle_override else self.produit.nom

    def montant_ht(self) -> Decimal:
        base = self.produit.prix * Decimal(self.quantite)
        if self.remise_pourcent and self.remise_pourcent > 0:
            base = base * (Decimal("100") - self.remise_pourcent) / Decimal("100")
        return base.quantize(Decimal("0.01"))

    def montant_tva(self) -> Decimal:
        taux = self.produit.taux_tva / Decimal("100")
        return (self.montant_ht() * taux).quantize(Decimal("0.01"))

    def montant_ttc(self) -> Decimal:
        return (self.montant_ht() + self.montant_tva()).quantize(Decimal("0.01"))
