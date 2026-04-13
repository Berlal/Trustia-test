# Generated manually for model upscale (Django 5.2)

import django.core.validators
import django.utils.timezone
from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="reference_interne",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="SKU / référence fournisseur",
                max_length=64,
            ),
        ),
        migrations.AddField(
            model_name="produit",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="produit",
            name="categorie",
            field=models.CharField(blank=True, db_index=True, default="", max_length=64),
        ),
        migrations.AddField(
            model_name="produit",
            name="actif",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name="produit",
            name="taux_tva",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("20.00"),
                help_text="TVA en % (affichage / exports)",
                max_digits=5,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0")),
                    django.core.validators.MaxValueValidator(Decimal("100")),
                ],
            ),
        ),
        migrations.AddField(
            model_name="produit",
            name="cree_le",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="produit",
            name="modifie_le",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="facture",
            name="statut",
            field=models.CharField(
                choices=[
                    ("brouillon", "Brouillon"),
                    ("envoyee", "Envoyée"),
                    ("payee", "Payée"),
                    ("annulee", "Annulée"),
                ],
                db_index=True,
                default="brouillon",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="facture",
            name="client_nom",
            field=models.CharField(blank=True, default="", max_length=255, verbose_name="client / raison sociale"),
        ),
        migrations.AddField(
            model_name="facture",
            name="client_email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AddField(
            model_name="facture",
            name="client_telephone",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
        migrations.AddField(
            model_name="facture",
            name="adresse_facturation",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="facture",
            name="devise",
            field=models.CharField(default="EUR", max_length=3),
        ),
        migrations.AddField(
            model_name="facture",
            name="notes_internes",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Visible équipe uniquement",
            ),
        ),
        migrations.AddField(
            model_name="facture",
            name="date_modification",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="factureligne",
            name="remise_pourcent",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0"),
                help_text="Remise ligne en %",
                max_digits=5,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0")),
                    django.core.validators.MaxValueValidator(Decimal("100")),
                ],
            ),
        ),
        migrations.AddField(
            model_name="factureligne",
            name="libelle_override",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Libellé facture si différent du produit",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="facture",
            name="reference",
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AddIndex(
            model_name="produit",
            index=models.Index(fields=["actif", "nom"], name="catalog_pro_actif_n_7b8c1e_idx"),
        ),
        migrations.AddIndex(
            model_name="facture",
            index=models.Index(
                fields=["statut", "-date_creation"],
                name="catalog_fac_statut_9f3a2b_idx",
            ),
        ),
    ]
