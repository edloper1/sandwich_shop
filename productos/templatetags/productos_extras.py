from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Devuelve el valor dividido por la clave dada.
    Uso: {{ value|split:"," }}
    """
    return value.split(key)

@register.filter  
def strip(value):
    """
    Elimina espacios en blanco al inicio y final.
    Uso: {{ value|strip }}
    """
    return value.strip()