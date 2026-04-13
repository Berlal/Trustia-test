from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_rename_catalog_fac_statut_9f3a2b_idx_catalog_fac_statut_66781c_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="facture",
            name="couleur_theme",
            field=models.CharField(
                default="#1a73e8",
                help_text="Couleur d’accent pour l’aperçu et le PDF (#RRGGBB).",
                max_length=7,
                validators=[
                    RegexValidator(
                        regex=r"^#[0-9A-Fa-f]{6}$",
                        message="La couleur doit être au format #RRGGBB.",
                    )
                ],
            ),
        ),
    ]
