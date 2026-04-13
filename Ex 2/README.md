# Exercice 2 — PInvoices (Django)

Application **Django 5.2** : **catalogue produits**, **factures** multi-lignes (quantités, TVA, remises), **pagination** des listes produits et factures. Accès **sans authentification** (données globales) ; l’**admin Django** (`/admin/`) reste protégée par un superutilisateur.

## Conformité sujet

| Exigence | Détail |
|----------|--------|
| Django | Oui (`ex2/`, app `catalog/`). |
| Produits | id, nom, prix, date de péremption (+ champs extra : réf., catégorie, TVA, catalogue…). |
| CRUD produits | Créer / modifier / supprimer / lister. |
| Pagination | `Paginator` sur listes **produits** et **factures**. |
| Factures | Plusieurs produits par facture, quantité par ligne (`FactureLigne`). |
| Détail facture | Lignes, totaux (HT / TVA / TTC, nombre d’articles). |
| Stack | Django, SQLite, HTML / CSS / JS. |

## Installation

```bash
cd "Ex 2"
python -m venv .venv
source .venv/activate          # Linux / macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optionnel — /admin/
python manage.py runserver
```

- App : **http://127.0.0.1:8000/** (tableau de bord).
- Admin : **http://127.0.0.1:8000/admin/** (Grappelli : `/grappelli/`).

Variables optionnelles (fichier **`.env`** à côté de `manage.py`, voir `.env.example`) : `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`.

## URLs principales (`catalog/urls.py`)

| URL | Rôle |
|-----|------|
| `/` | Tableau de bord |
| `/catalogue/`, `/produits/` | Liste produits (filtres + pagination) |
| `/produits/nouveau/`, `…/modifier/<pk>/`, `…/supprimer/<pk>/` | CRUD |
| `/factures/`, `/factures/nouvelle/` | Liste + création facture |
| `/factures/<pk>/` | Détail + totaux |
| `/factures/<pk>/pdf/` | PDF (si `weasyprint` installé) |

## Modèles (`catalog/models.py`)

- **`Produit`** : nom, prix, date de péremption, etc. (pas de multi-tenant).
- **`Facture`** : client, statut, lignes via **`FactureLigne`** (`produit`, `quantite`, remise, libellé optionnel). Unicité `(facture, produit)` par facture.

## Données de démo

La migration **`0004`** crée l’utilisateur **`invite`** / mot de passe **`invite`** et un jeu **TEST** (produits + factures), via le **schéma historique** des migrations.  
`catalog/demo_seed.py` sert surtout à un éventuel appel manuel (idempotent si `TEST #1` existe).

## Fichiers utiles

`manage.py`, `requirements.txt`, `ex2/settings.py`, `catalog/models.py`, `views.py`, `forms.py`, `admin.py`, `templates/`, `static/catalog/`.

## Sécurité (production)

Changer `SECRET_KEY`, désactiver `DEBUG`, restreindre `ALLOWED_HOSTS`, ne pas exposer l’admin sans protection. Ne pas committer `.env` ni `db.sqlite3`.
