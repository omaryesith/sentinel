#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Apply migrations automatically on startup (Common practice in Dev, be careful in Prod)
python manage.py migrate

# Start development server listening on all interfaces
python manage.py runserver 0.0.0.0:8000
