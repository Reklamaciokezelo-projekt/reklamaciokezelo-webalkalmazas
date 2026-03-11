"""
pytest conftest: Tesztelési Flask alkalmazás fixture-ok.
SQLite in-memory adatbázist használ – PostgreSQL connection nem szükséges.

Megközelítés:
  Az SQLite in-memory DB per-connection: ha két különböző connection nyílik
  ugyanarra az URI-ra, két KÜLÖN üres adatbázist kapnak. Ezért egyetlen
  megosztott connection-t kell használni minden session-höz (teszt + app kérés).
  Az SQLAlchemy "engine_connect" eseménnyel kényszerítjük az összes új
  connection-t arra, hogy ugyanazt a nyitott connection-t használja.
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session

from application import app as flask_app, db as _db, bcrypt
from application.models import User, Role, Position, Customer, Product, DefectType, Department, Status


@pytest.fixture(scope='session')
def app():
    """
    Session-szintű Flask app fixture.
    Egyetlen megosztott SQLite connection-t használ az engine-ben,
    így a seeded adatok minden sessionből (teszt + app kérés) láthatók.
    """
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'RESEND_API_KEY': 'test-api-key',
        'MAIL_FROM': 'test@example.com',
        'PASSWORD_RESET_TOKEN_EXPIRY': 3600,
    })

    # --- Egyetlen megosztott connection (SQLite in-memory per-connection) ---
    sqlite_engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
    )
    shared_connection = sqlite_engine.connect()

    # --- Minden új engine.connect()-et ráirányítunk a megosztott connectionre ---
    @event.listens_for(sqlite_engine, 'connect')
    def connect(dbapi_conn, connection_record):
        pass  # Az összes connection az engine-en belül megosztott

    # --- Az engine-t és a session-t felülírjuk a teszt scope-ra ---
    with flask_app.app_context():
        # Engine csere FSQLA 3.x-ben
        _db.engines[flask_app] = sqlite_engine

        # Táblák létrehozása
        _db.metadata.create_all(shared_connection)

        # Session átirányítása a megosztott connection-re
        TestSession = scoped_session(
            sessionmaker(bind=shared_connection, autocommit=False, autoflush=False)
        )
        _db.session = TestSession

        _seed_test_data()
        yield flask_app

        TestSession.remove()
        _db.metadata.drop_all(shared_connection)
        shared_connection.close()
        sqlite_engine.dispose()


def _seed_test_data():
    """Minimális tesztadatok feltöltése (szerepkör, pozíció, felhasználó és alapvető entitások)."""
    # Szerepkörök és Pozíciók
    role = Role(name='user', display_name='Felhasználó')
    admin_role = Role(name='super_user', display_name='Szuperfelhasználó')
    position = Position(name='test', display_name='Teszt')
    _db.session.add_all([role, admin_role, position])
    _db.session.commit()

    # Hitelesítési Teszt Felhasználó
    hashed = bcrypt.generate_password_hash('OldPassword1!').decode('utf-8')
    user = User(
        surname='Teszt',
        forename='Elek',
        username='tesztelek',
        email='teszt@example.com',
        password=hashed,
        role_id=role.id,
        position_id=position.id,
    )
    _db.session.add(user)
    _db.session.commit()

    # Reklamáció Referencia Adatok (Teszteléshez)
    customer = Customer(name='teszt_vevo', display_name='Teszt Vevő Kft.')
    product = Product(name='teszt_termek', display_name='Teszt Termék')
    defect = DefectType(name='teszt_hiba', display_name='Teszt Hiba')
    dept = Department(name='teszt_uzem', display_name='Teszt Üzemegység')
    status_foly = Status(name='folyamatban', display_name='Folyamatban')
    status_elf = Status(name='elfogadva', display_name='Elfogadva')
    
    _db.session.add_all([customer, product, defect, dept, status_foly, status_elf])
    _db.session.commit()



@pytest.fixture
def client(app):
    """Flask tesztkliense."""
    return app.test_client()
