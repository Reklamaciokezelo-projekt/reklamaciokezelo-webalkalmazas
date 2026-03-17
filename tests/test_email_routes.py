"""
Tesztek az e-mail útvonalakhoz (elfelejtett jelszó, jelszó visszaállítása).
A resend.Emails.send mocking-gal van helyettesítve, így nem küld valós e-mailt.
A fixture-ok a conftest.py-ban vannak definiálva.
"""
import pytest
from unittest.mock import patch, MagicMock
from application import app as flask_app, db, bcrypt
from application.models import User
from application.utils.email_service import generate_reset_token


# ----------------------------------------------------------------------
# ELFELEJTETT JELSZÓ – GET
# ----------------------------------------------------------------------

def test_forgot_password_get(client):
    """GET /forgot_password – 200-as választ ad és a form megjelenik."""
    response = client.get('/forgot_password')
    print("HEADERS:", response.headers)
    assert response.status_code == 200
    assert 'Elfelejtett jelszó'.encode('utf-8') in response.data


# ----------------------------------------------------------------------
# ELFELEJTETT JELSZÓ – POST ismeretlen e-mail
# ----------------------------------------------------------------------

def test_forgot_password_unknown_email(client):
    """
    POST /forgot_password ismeretlen e-mail esetén:
    – 302-es átirányítás a login oldalra
    – Ugyanaz a tájékoztató flash üzenet (e-mail enumeration elleni védelem)
    – Az e-mail küldés nem hívódik meg
    """
    with patch('application.utils.email_service.resend.Emails.send') as mock_send:
        response = client.post('/forgot_password', data={
            'email': 'nemletezik@example.com'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'hamarosan megérkezik'.encode('utf-8') in response.data
        mock_send.assert_not_called()


# ----------------------------------------------------------------------
# ELFELEJTETT JELSZÓ – POST ismert e-mail
# ----------------------------------------------------------------------

def test_forgot_password_known_email_sends_email(client, app):
    """
    POST /forgot_password ismert e-mail esetén:
    – Ugyanaz a tájékoztató flash üzenet
    – A resend.Emails.send meghívódik egyszer
    """
    with patch('application.utils.email_service.resend.Emails.send') as mock_send:
        mock_send.return_value = MagicMock()
        response = client.post('/forgot_password', data={
            'email': 'teszt@example.com'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'hamarosan megérkezik'.encode('utf-8') in response.data
        mock_send.assert_called_once()


# ----------------------------------------------------------------------
# JELSZÓ VISSZAÁLLÍTÁSA – GET érvénytelen tokennel
# ----------------------------------------------------------------------

def test_reset_password_invalid_token(client):
    """
    GET /reset_password/<érvénytelen_token>:
    – Átirányít a forgot_password oldalra
    – Hibaüzenetet jelenít meg
    """
    response = client.get('/reset_password/ez-egy-ervenytelen-token', follow_redirects=True)
    assert response.status_code == 200
    assert 'érvénytelen vagy lejárt'.encode('utf-8') in response.data


# ----------------------------------------------------------------------
# JELSZÓ VISSZAÁLLÍTÁSA – GET érvényes tokennel
# ----------------------------------------------------------------------

def test_reset_password_valid_token_get(client, app):
    """
    GET /reset_password/<érvényes_token>:
    – 200-as választ ad
    – Az új jelszó form megjelenik
    """
    with app.app_context():
        token = generate_reset_token('teszt@example.com')

    response = client.get(f'/reset_password/{token}')
    assert response.status_code == 200
    assert 'Új jelszó beállítása'.encode('utf-8') in response.data


# ----------------------------------------------------------------------
# JELSZÓ VISSZAÁLLÍTÁSA – POST érvényes tokennel
# ----------------------------------------------------------------------

def test_reset_password_valid_token_post(client, app):
    """
    POST /reset_password/<érvényes_token> helyes jelszóval:
    – Átirányít a login oldalra
    – A felhasználó be tud jelentkezni az új jelszóval
    """
    with app.app_context():
        token = generate_reset_token('teszt@example.com')

    response = client.post(f'/reset_password/{token}', data={
        'new_password': 'UjJelszó123!',
        'confirm_password': 'UjJelszó123!',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'sikeresen megváltozott'.encode('utf-8') in response.data

    # --- Ellenőrizzük, hogy tényleg megváltozott-e a jelszó az adatbázisban ---
    with app.app_context():
        user = User.query.filter_by(email='teszt@example.com').first()
        assert bcrypt.check_password_hash(user.password, 'UjJelszó123!')
