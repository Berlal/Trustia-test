"""Exercice 3 (ex 2)"""

MENU = {
    "--- entrées ---": [
        {"nom": "salade césar", "prix": 8, "disponible": True},
        {"nom": "soupe du jour", "prix": 6, "disponible": False},
    ],
    "--- plats ---": [
        {"nom": "steak frites", "prix": 15, "disponible": True},
        {"nom": "poisson grillé", "prix": 14, "disponible": True},
        {"nom": "plat du chef", "prix": 18, "disponible": False},
    ],
    "--- desserts ---": [
        {"nom": "tiramisu", "prix": 7, "disponible": True},
        {"nom": "glace", "prix": 5, "disponible": True},
        {"nom": "dessert mystere", "prix": 9, "disponible": False},
    ]
}


def afficher_categorie(nom: str, plats: list[dict]) -> None:
    print(f"\n{nom.lower()}")

    for plat in plats:
        if not plat["disponible"]:
            continue

        nom_plat = plat["nom"].lower()
        prix = f"{plat['prix']}€"

        print(f"{nom_plat} - {prix}")


def main():
    for categorie, plats in MENU.items():
        afficher_categorie(categorie, plats)


if __name__ == "__main__":
    main()