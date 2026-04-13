from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def eur_fr(value) -> str:
    """Formate un montant en euros style FR (virgule décimale)."""
    if value is None or value == "":
        return "—"
    try:
        v = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError, ValueError):
        return "—"
    s = f"{v:.2f}".replace(".", ",")
    return f"{s}\u00a0€"
