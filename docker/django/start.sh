#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Aplicar migraciones automáticamente al arrancar (Práctica común en Dev, cuidado en Prod)
python manage.py migrate

# Arrancar servidor de desarrollo escuchando en todas las interfaces
python manage.py runserver 0.0.0.0:8000
