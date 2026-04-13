"""Exercice 1"""

MAX_WIDTH = 100


PHRASES = {
    "m1": "Le code propre facilite la maintenance",
    "m2": "Tester souvent évite beaucoup d erreurs",
    "m3": "cette phrase ne doit pas s afficher",
    "m4": "Un bon code doit rester simple et clair",
    "m5": "La simplicité améliore la qualité du code",
    "m6": "Refactoriser améliore la compréhension",
}

# Phrases qui n'apparaissent pas 
INTERDITS = {
    "cette phrase ne doit pas s afficher",
    "un bon code doit rester simple et clair",
}

# Ordre des blocs 
BLOCS = [
    ["m1"],
    ["m2", "m3"],
    ["m3", "m4", "m5", "m6"],
]


def lignes_a_afficher(cles: list[str]) -> list[str]:
    """Retourne les lignes en minuscules, sans les phrases interdites."""
    out = []
    for k in cles:
        t = PHRASES[k].lower()
        if t in INTERDITS:
            continue
        out.append(t)
    return out


def afficher_bloc(lignes: list[str]) -> None:
    if not lignes:
        return
    largeur_interieure = MAX_WIDTH - 4
    print("-" * MAX_WIDTH)
    for ligne in lignes:
        if len(ligne) > largeur_interieure:
            ligne = ligne[:largeur_interieure]
        print(f"| {ligne.rjust(largeur_interieure)} |")
    print("-" * MAX_WIDTH)


def main() -> None:
    for cles in BLOCS:
        afficher_bloc(lignes_a_afficher(cles))


if __name__ == "__main__":
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
