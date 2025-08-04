#!/bin/sh

set -e

echo "Running database migrations..."
python -m alembic -c /code/alembic.ini upgrade head

echo "Migrations complete. Starting application..."
exec "$@"
