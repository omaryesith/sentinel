#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Calculate optimal workers: 2 * CPU cores + 1
WORKERS=${GUNICORN_WORKERS:-3}
TIMEOUT=${GUNICORN_TIMEOUT:-120}

echo "Starting Gunicorn with $WORKERS workers..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $WORKERS \
    --timeout $TIMEOUT \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance
