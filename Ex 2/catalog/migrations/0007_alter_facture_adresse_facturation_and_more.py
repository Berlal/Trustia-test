from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Aligne l’état du champ avec le modèle actuel (sans default explicite sur TextField).
    Si cette migration existait déjà chez vous avec le même nom, le contenu doit rester équivalent.
    """

    dependencies = [
        ("catalog", "0006_facture_couleur_theme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facture",
            name="adresse_facturation",
            field=models.TextField(blank=True),
        ),
    ]
