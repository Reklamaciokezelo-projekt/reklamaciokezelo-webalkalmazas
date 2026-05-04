"""
A webalkalmazás központi konfigurációs modulja.
Feladata a környezeti változók, például adatbázis-kapcsolat, titkosítási kulcsok, API hozzáférések
biztonságos beolvasása.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --- Környezeti változók betöltése ---
# A rendszer több lehetséges útvonalról próbálja beolvasni a konfigurációt,
# támogatva mind a Docker konténeres, mind a lokális fejlesztői környezeteket.
_config_dir = Path(__file__).resolve().parent
load_dotenv(Path("/project") / "docker.env")  # Konténeren belüli Docker Compose konfiguráció
load_dotenv(_config_dir / "docker.env")       # Lokális Docker Compose konfiguráció
load_dotenv(_config_dir / ".env")             # Hagyományos lokális fejlesztői konfiguráció

# --- Alapvető biztonsági és adatbázis beállítások ---
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Ha lokálisan futtatjuk a Flask alkalmazást (nem a Docker konténerben), 
# akkor a 'db' host nem elérhető, helyette 'localhost'-ot kell használni.
if not Path("/.dockerenv").exists() and SQLALCHEMY_DATABASE_URI and "@db:" in SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("@db:", "@localhost:")

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
