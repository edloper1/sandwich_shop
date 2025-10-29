import os
import sys

# Load Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandwich_shop.settings')
# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import django
django.setup()

from django.template.loader import get_template

ROOT = os.path.join(os.path.dirname(__file__), '..')
TEMPLATES_DIR = os.path.join(ROOT, 'templates')

errors = []

for dirpath, _, filenames in os.walk(TEMPLATES_DIR):
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(dirpath, fname), TEMPLATES_DIR).replace('\\', '/')
        try:
            get_template(rel)
        except Exception as e:
            print('ERROR loading', rel, '->', repr(e))
            errors.append((rel, e))

if not errors:
    print('ALL_TEMPLATES_OK')
    sys.exit(0)
else:
    print('\nFound %d template errors' % len(errors))
    sys.exit(1)
