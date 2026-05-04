#!/bin/sh
# --- A webalkalmazás konténerének indítását vezérlő szkript (Entrypoint). ---
set -e
cd /app
if [ "$#" -gt 0 ]; then
  exec "$@"
fi
flask --app application db upgrade
exec gunicorn -w 2 -b 0.0.0.0:8000 application:app
