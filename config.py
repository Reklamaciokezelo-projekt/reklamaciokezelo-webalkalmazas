import os
from dotenv import load_dotenv

# Betölti a lokális .env fájlt (éles szerveren ez a fájl nem lesz ott, azt a Render adja)
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# A Render postgres:// formátumot ad, de a SQLAlchemy >= 1.4 postgresql://-t vár
if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_HEADERS = ["X-CSRFToken"]

# --- E-mail szolgáltatás (Resend) ---
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
MAIL_FROM = os.environ.get('MAIL_FROM')
PASSWORD_RESET_TOKEN_EXPIRY = int(os.environ.get('PASSWORD_RESET_TOKEN_EXPIRY', 3600))  # Másodpercben: 1 óra
# Értesítendő e-mail cím új/módosított/törölt reklamáció esetén
REKLAMACIOS_KOR_EMAIL = os.environ.get('REKLAMACIOS_KOR_EMAIL')
