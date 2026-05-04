#!/bin/sh
set -e

# A Docker környezet automatikus inicializálását végző szkript.
# Feladata a szükséges környezeti változók (pl. jelszavak, titkosítási kulcsok) legenerálása
# és azok elmentése egy dedikált 'docker.env' fájlba. Ez a megoldás kiküszöböli
# a Windows platformon előforduló fájlrendszer- és hozzáférési problémákat.

DOCKER_ENV="/work/docker.env"
LEGACY_ENV="/work/.env"

# --- Hibaellenőrzés: Könyvtárként létrejött környezeti fájlok kiszűrése (Windows Docker bind-mount sajátosság) ---
if [ -d "$LEGACY_ENV" ]; then
  echo "init-env: HIBA: A(z) '$LEGACY_ENV' egy könyvtár a gazdagépen. Töröld vagy nevezd át, majd próbáld újra. Lásd: README (Windows)."
  exit 1
fi

if [ -d "$DOCKER_ENV" ]; then
  echo "init-env: HIBA: A docker.env egy könyvtár a gazdagépen. Töröld a mappát a projekt gyökeréből, majd próbáld újra. Lásd: README."
  exit 1
fi

# --- Ha a környezeti fájl már létezik, a szkript futása megszakad, hogy megőrizze a korábbi beállításokat ---
if [ -f "$DOCKER_ENV" ]; then
  echo "init-env: A docker.env fájl már létezik, generálás kihagyva."
  exit 0
fi

# --- Visszafelé kompatibilitás: meglévő .env fájl tartalmának átmásolása ---
if [ -f "$LEGACY_ENV" ]; then
  cp "$LEGACY_ENV" "$DOCKER_ENV"
  echo "init-env: .env fájl másolva a docker.env fájlba (migráció meglévő fájlból)."
  exit 0
fi

# --- Dinamikus hitelesítő adatok és titkosítási kulcsok generálása az OpenSSL segítségével ---
POSTGRES_USER="reklamacio_kezelo"
POSTGRES_PASSWORD=$(openssl rand -hex 16)
POSTGRES_DB="reklamaciokezelo_db"
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"

# --- Környezeti változók kiírása a docker.env fájlba ---
{
  printf '%s\n' "# Automatikusan generált konfiguráció. A pgdata kötet és ezen fájl együttes kezelése szükséges."
  printf '%s\n' ""
  printf '%s\n' "# --- PostgreSQL ---"
  printf '%s\n' "POSTGRES_USER=${POSTGRES_USER}"
  printf '%s\n' "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}"
  printf '%s\n' "POSTGRES_DB=${POSTGRES_DB}"
  printf '%s\n' ""
  printf '%s\n' "DATABASE_URL=${DATABASE_URL}"
  printf '%s\n' ""
  printf '%s\n' "# --- Flask ---"
  printf '%s\n' "SECRET_KEY=${SECRET_KEY}"
  printf '%s\n' ""
  printf '%s\n' "# --- E-mail küldési beállítások (Resend API) ---"
  printf '%s\n' "RESEND_API_KEY="
  printf '%s\n' "MAIL_FROM="
  printf '%s\n' "REKLAMACIOS_KOR_EMAIL="
  printf '%s\n' ""
  printf '%s\n' "# A Flask adatbázis-migrációjához (flask db upgrade) szükséges konfiguráció"
  printf '%s\n' "FLASK_APP=application"
  printf '%s\n' ""
  printf '%s\n' "WEB_PORT=8000"
} > "$DOCKER_ENV"

echo "init-env: docker.env fájl sikeresen létrehozva."
