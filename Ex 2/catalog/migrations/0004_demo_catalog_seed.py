# Démo : compte invite + produits/factures (état schéma = post-0003, sans import models actuels).

from datetime import date, timedelta
from decimal import Decimal

from django.db import migrations


def seed_demo_pour_tous(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Produit = apps.get_model("catalog", "Produit")
    Facture = apps.get_model("catalog", "Facture")
    FactureLigne = apps.get_model("catalog", "FactureLigne")

    invite, created = User.objects.get_or_create(
        username="invite",
        defaults={"email": "invite@pinvoices.demo", "is_active": True},
    )
    if created or not invite.has_usable_password():
        invite.set_password("invite")
        invite.save()

    statuts = ["brouillon", "envoyee", "payee", "annulee"]

    for user in User.objects.all():
        if Produit.objects.filter(proprietaire_id=user.pk, nom="TEST #1").exists():
            continue

        produits = []
        for i in range(1, 11):
            produits.append(
                Produit.objects.create(
                    proprietaire_id=user.pk,
                    nom=f"TEST #{i}",
                    reference_interne=f"D{i:02d}",
                    description="Test PInvoices",
                    categorie="Démo",
                    prix=Decimal("10.00") + Decimal(i),
                    date_peremption=date.today() + timedelta(days=365 + i),
                    actif=True,
                    taux_tva=Decimal("20.00"),
                )
            )

        for i in range(10):
            facture = Facture.objects.create(
                proprietaire_id=user.pk,
                reference=f"REF-TEST-{i + 1:02d}",
                statut=statuts[i % len(statuts)],
                client_nom=f"Client TEST {i + 1}",
                client_email=f"client.test{i + 1}@demo.pinvoices.local",
                client_telephone=f"01 23 45 67 {i:02d}",
                adresse_facturation=f"{i + 1} rue Démo\n7500{i % 10} Paris",
                devise="EUR",
                notes_internes="Test PInvoices",
            )
            FactureLigne.objects.create(
                facture=facture,
                produit=produits[i],
                quantite=1,
                remise_pourcent=Decimal("0"),
                libelle_override="",
            )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_proprietaire_multi_tenant"),
    ]

    operations = [
        migrations.RunPython(seed_demo_pour_tous, noop_reverse),
    ]
