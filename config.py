"""
A webalkalmazás központi konfigurációs modulja.
Feladata a környezeti változók, például adatbázis-kapcsolat, titkosítási kulcsok, API hozzáférések
biztonságos beolvasása.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --- Környezeti változók betöltése ---
# A rendszer a futási környezettől függően dinamikusan választja ki a konfigurációs fájlokat.
# Docker konténeren belül a 'docker.env' fájlokat kezeli prioritásként, 
# míg lokális fejlesztői környezetben a szabványos '.env' fájlt olvassa be.
_config_dir = Path(__file__).resolve().parent
_in_docker = Path("/.dockerenv").exists()
if _in_docker:
    load_dotenv(Path("/project") / "docker.env")
    load_dotenv(_config_dir / "docker.env")
load_dotenv(_config_dir / ".env")

# --- Alapvető biztonsági és adatbázis beállítások ---
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Kompatibilitási javítás: Az SQLAlchemy újabb verziói a 'postgresql://' sémát követelik meg,
# ezért a régebbi 'postgres://' formátumú URI-kat konvertálni kell.
if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_HEADERS = ["X-CSRFToken"]

# --- Külső szolgáltatások (Resend E-mail API) ---
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
MAIL_FROM = os.environ.get('MAIL_FROM')
PASSWORD_RESET_TOKEN_EXPIRY = int(os.environ.get('PASSWORD_RESET_TOKEN_EXPIRY', 3600))  # Érvényességi idő (másodperc)

# --- Értesítési beállítások ---
REKLAMACIOS_KOR_EMAIL = os.environ.get('REKLAMACIOS_KOR_EMAIL')
