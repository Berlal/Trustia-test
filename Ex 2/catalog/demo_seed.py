# Démo : 10 produits + 10 factures (idempotent si TEST #1 existe).

from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction

from .models import Facture, FactureLigne, Produit

DEMO_FIRST_PRODUCT = "TEST #1"


@transaction.atomic
def seed_demo_catalog(utilisateur=None):
    """Param ``utilisateur`` ignoré (compat. migration 0004)."""
    if Produit.objects.filter(nom=DEMO_FIRST_PRODUCT).exists():
        return False

    produits = []
    for i in range(1, 11):
        produits.append(
            Produit.objects.create(
                nom=f"TEST #{i}",
                reference_interne=f"D{i:02d}",
                description="Test PInvoices",
                categorie="Démo",
                prix=Decimal("10.00") + Decimal(i),
                date_peremption=date.today() + timedelta(days=365 + i),
                actif=True,
                au_catalogue=True,
                taux_tva=Decimal("20.00"),
            )
        )

    statuts = [
        Facture.Statut.BROUILLON,
        Facture.Statut.ENVOYEE,
        Facture.Statut.PAYEE,
        Facture.Statut.ANNULEE,
    ]

    for i in range(10):
        facture = Facture.objects.create(
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

    return True
