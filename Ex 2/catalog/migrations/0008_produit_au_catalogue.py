from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_alter_facture_adresse_facturation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="au_catalogue",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Si coché, le produit est proposé dans le catalogue (liste) et dans les lignes de facture. "
                "Une seule case à cocher, identique partout.",
                verbose_name="au catalogue",
            ),
        ),
        migrations.AddIndex(
            model_name="produit",
            index=models.Index(
                fields=["proprietaire", "actif", "au_catalogue"],
                name="catalog_pro_prop_act_auc_idx",
            ),
        ),
    ]
