"""Exercice 1 - Mis à jour"""

MAX_WIDTH = 100

# Tout est centralisé

ENSEMBLE = [
    {
        "title": "bloc 1",
        "lines": [
            {"text": "Le code propre facilite la maintenance", "show": True}
        ]
    },
    {
        "title": "bloc 2",
        "lines": [
            {"text": "Tester souvent evite beaucoup d erreurs", "show": True},
            {"text": "Cette phrase ne doit pas s afficher", "show": False}
        ]
    },
    {
        "title": "bloc 3",
        "lines": [
            {"text": "Cette phrase ne doit pas s afficher", "show": False},
            {"text": "Un bon code doit rester simple et clair", "show": True},
            {"text": "La simplicite ameliore la qualite du code", "show": True},
            {"text": "Refactoriser ameliore la compréhension", "show": True},
        ]
    }
]


def afficher_bloc(lignes: list[dict]) -> None:
    if not lignes:
        return

    largeur_interieure = MAX_WIDTH - 4

    print("-" * MAX_WIDTH)

    for ligne in lignes:
        texte = ligne["text"].lower()

        if len(texte) > largeur_interieure:
            texte = texte[:largeur_interieure]

        print(f"| {texte.rjust(largeur_interieure)} |")

    print("-" * MAX_WIDTH)


def main():
    for bloc in ENSEMBLE:
        visible_lines = [l for l in bloc["lines"] if l["show"]]
        afficher_bloc(visible_lines)


if __name__ == "__main__":
    main()