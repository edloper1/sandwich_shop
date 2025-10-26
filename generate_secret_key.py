#!/usr/bin/env python
"""
Script para generar una nueva SECRET_KEY para Django
Úsala en las variables de entorno de Vercel
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("=" * 60)
    print("🔑 NUEVA SECRET_KEY GENERADA:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("📋 Copia esta clave y úsala como variable de entorno SECRET_KEY en Vercel")
    print("⚠️  NUNCA la subas a GitHub o la compartas públicamente")
    print("=" * 60)