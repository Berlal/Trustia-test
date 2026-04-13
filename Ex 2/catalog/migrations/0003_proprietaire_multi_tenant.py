# Generated manually — rattachement des données utilisateur

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def rattacher_donnees_existantes(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Produit = apps.get_model("catalog", "Produit")
    Facture = apps.get_model("catalog", "Facture")
    proprietaire = User.objects.order_by("pk").first()
    if proprietaire is None:
        proprietaire = User(
            username="donnees_legacy",
            email="",
            is_active=False,
            is_staff=False,
            is_superuser=False,
        )
        proprietaire.set_unusable_password()
        proprietaire.save()
    Produit.objects.filter(proprietaire__isnull=True).update(proprietaire=proprietaire)
    Facture.objects.filter(proprietaire__isnull=True).update(proprietaire=proprietaire)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0002_produit_facture_upscale"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="proprietaire",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="produits",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="facture",
            name="proprietaire",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="factures",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(rattacher_donnees_existantes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="produit",
            name="proprietaire",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="produits",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="facture",
            name="proprietaire",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="factures",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
