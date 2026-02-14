SECRET_KEY = 'dijsilmeslmelwovwnajpowJ' # éles környezetben környezeti változóba illik helyezni (pl. os.environ.get('SECRET_KEY')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5432/flask_app_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_HEADERS = ["X-CSRFToken"]