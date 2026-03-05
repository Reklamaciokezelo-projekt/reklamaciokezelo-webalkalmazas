"""
Tesztek a reklamáció értesítő e-mail szolgáltatáshoz.
Nem küld valódi e-mailt, a resend.Emails.send mockolva van.
"""
import pytest
from unittest.mock import patch, MagicMock
from application.utils.email_service import send_reklamacio_notification_email
from application.models import Reklamacio, User, Department, Customer, Product, DefectType, Status
from datetime import date

def test_send_reklamacio_notification_email_sikeres(app):
    """
    Teszteli, hogy az e-mail küldő függvény meghívja tesztkörnyezetben a Resend API-t.
    """
    with app.app_context():
        # --- Létrehozunk egy mock reklamáció objektumot hogy ne kelljen DB-t feltölteni ---
        mock_user = MagicMock(spec=User)
        mock_user.surname = "Teszt"
        mock_user.forename = "Elek"
        
        mock_szotar = MagicMock()
        mock_szotar.display_name = "Teszt"

        mock_reklamacio = MagicMock(spec=Reklamacio)
        mock_reklamacio.complaint_number = "REK-2026-001"
        mock_reklamacio.quantity = 5
        mock_reklamacio.customer = mock_szotar
        mock_reklamacio.product = mock_szotar
        mock_reklamacio.defect_type = mock_szotar
        mock_reklamacio.status = mock_szotar
        mock_reklamacio.user = mock_user

        with patch('application.utils.email_service.resend.Emails.send') as mock_send:
            mock_send.return_value = MagicMock()
            
            # --- Függvény meghívása ---
            eredmeny = send_reklamacio_notification_email("Új", mock_reklamacio)
            
            # --- Ellenőrzés ---
            assert eredmeny is True
            mock_send.assert_called_once()
            
            # --- Ellenőrizzük, hogy a hívás paraméterei tartalmazzák-e a megadott e-mailt ---
            hivas_args = mock_send.call_args[0][0]
            assert hivas_args['to'] == app.config['REKLAMACIOS_KOR_EMAIL']
            assert "Új reklamáció" in hivas_args['subject']
            assert "REK-2026-001" in hivas_args['subject']


def test_send_reklamacio_notification_email_nincs_cim(app):
    """
    Teszteli, hogy ha nincs REKLAMACIOS_KOR_EMAIL konfigurálva, akkor kilép-e False értékkel.
    """
    with app.app_context():
        # --- E-mail cím konfiguráció törlése a teszt erejéig ---
        eredeti_email = app.config.get('REKLAMACIOS_KOR_EMAIL')
        app.config['REKLAMACIOS_KOR_EMAIL'] = None
        
        mock_reklamacio = MagicMock(spec=Reklamacio)
        
        with patch('application.utils.email_service.resend.Emails.send') as mock_send:
            eredmeny = send_reklamacio_notification_email("Módosított", mock_reklamacio)
            
            assert eredmeny is False
            mock_send.assert_not_called()
            
        # Visszaállítás
        app.config['REKLAMACIOS_KOR_EMAIL'] = eredeti_email
