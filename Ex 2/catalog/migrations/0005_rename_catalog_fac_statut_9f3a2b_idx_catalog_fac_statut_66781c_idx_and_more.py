# Alignement des noms d’index avec Django 5.2 (auto-généré côté détection)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_demo_catalog_seed"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="facture",
            new_name="catalog_fac_statut_66781c_idx",
            old_name="catalog_fac_statut_9f3a2b_idx",
        ),
        migrations.RenameIndex(
            model_name="produit",
            new_name="catalog_pro_actif_e40510_idx",
            old_name="catalog_pro_actif_n_7b8c1e_idx",
        ),
    ]
