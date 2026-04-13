# Retrait proprietaire (catalogue global).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_produit_au_catalogue"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="produit",
            name="catalog_pro_prop_act_auc_idx",
        ),
        migrations.RemoveField(
            model_name="facture",
            name="proprietaire",
        ),
        migrations.RemoveField(
            model_name="produit",
            name="proprietaire",
        ),
        migrations.AddIndex(
            model_name="produit",
            index=models.Index(
                fields=["actif", "au_catalogue"],
                name="catalog_pro_actif_auc_idx",
            ),
        ),
    ]
