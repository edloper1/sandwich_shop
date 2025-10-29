from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter(name='format_mxn')
def format_mxn(value):
    """Formatea un número como moneda MXN usando punto decimal y 2 decimales.

    Ejemplo: 79 -> "79.00" ; 79.5 -> "79.50"
    Si el valor es None o no convertible, devuelve cadena vacía.
    """
    if value is None:
        return ''
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        try:
            d = Decimal(float(value))
        except Exception:
            return ''

    # Normalizar y formatear con 2 decimales usando punto
    return f"{d.quantize(Decimal('0.01')):f}" if d != d.to_integral() else f"{d:.2f}"
