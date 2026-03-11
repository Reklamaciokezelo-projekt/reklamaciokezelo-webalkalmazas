import pytest
from flask import url_for
from application.models import User
from application import db

def test_login_success(client, app):
    """
    Teszteli a sikeres bejelentkezést a `tesztelek` felhasználóval.
    """
    with app.test_request_context():
        # A teszt adatok a conftest.py-ból jönnek (tesztelek / OldPassword1!)
        response = client.post(url_for('login'), data={
            'email': 'teszt@example.com',
            'password': 'OldPassword1!'
        }, follow_redirects=False)

        # Sikeres login után átirányítás a dashboardra
        assert response.status_code == 302
        assert '/home' in response.headers['Location'] or '/' in response.headers['Location']

def test_login_failure(client, app):
    """
    Teszteli a hibás jelszóval történő bejelentkezési kísérletet.
    """
    with app.test_request_context():
        response = client.post(url_for('login'), data={
            'email': 'teszt@example.com',
            'password': 'HibasJelszo!'
        }, follow_redirects=True)

        # Sikertelen login esetén a login oldalon maradunk, egy hibaüzenettel.
        assert response.status_code == 401 or response.status_code == 200
        # A válaszban benne kell lennie a HTML űrlapnak
        assert b'login' in response.data.lower() or b'bejelentkez' in response.data.lower()

def test_register_user_success(client, app):
    """
    Teszteli egy új felhasználó létrehozását (Adminisztrátorként).
    """
    with app.test_request_context():
        # 1. Bejelentkezés a tesztelek felhasználóval
        # A regisztrációhoz jelenleg admin ROLE kell.
        
        from application.models import Role, Position
        admin_role = Role.query.filter_by(name='admin').first()
        
        # Ha a conftestben még nincs 'admin', akkor felvesszük a teszt idejére
        if not admin_role:
            admin_role = Role(name='admin', display_name='Adminisztrátor')
            db.session.add(admin_role)
            db.session.commit()
            
        pos = Position.query.first()
        
        # Ideiglenesen felruházzuk a tesztelek usert admin joggal a teszt idejére
        admin_user = User.query.filter_by(username='tesztelek').first()
        admin_user.role_id = admin_role.id
        db.session.commit()

        # Bejelentkezünk
        client.post(url_for('login'), data={
            'email': 'teszt@example.com',
            'password': 'OldPassword1!'
        })

        # 2. Új felhasználó létrehozása
        response = client.post(url_for('register'), data={
            'surname': 'Új',
            'forename': 'Felhasználó',
            'username': 'uj_user_1',
            'email': 'uj_user@test.hu',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
            'role': admin_role.id,
            'position': pos.id,
            'submit': True
        }, follow_redirects=True)

        # 3. Ellenőrzés, hogy a felhasználó bekerült-e az adatbázisba
        new_user = User.query.filter_by(username='uj_user_1').first()
        assert new_user is not None, f"Response volt: {response.data.decode('utf-8')[:500]}"
        assert new_user.email == 'uj_user@test.hu'
        assert response.status_code == 200
