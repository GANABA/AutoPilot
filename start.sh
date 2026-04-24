#!/bin/sh
set -e
echo "Lancement des migrations Alembic..."
alembic upgrade head
echo "Migrations OK. Démarrage de l'API..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
