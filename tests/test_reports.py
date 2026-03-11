import pytest
from flask import url_for
from datetime import date, timedelta
from application.models import User, Role, Reklamacio, DefectType, Customer, Product, Department, Status
from unittest.mock import patch

@pytest.fixture
def setup_super_user(app):
    """Fixture to ensure a super_user role and user exist and are logged in."""
    with app.test_request_context():
        from application import db
        super_role = Role.query.filter_by(name='super_user').first()
        if not super_role:
            super_role = Role(name='super_user', display_name='Szuperfelhasználó')
            db.session.add(super_role)
            db.session.commit()
            
        test_user = User.query.filter_by(username='tesztelek').first()
        if test_user:
            test_user.role_id = super_role.id
            db.session.commit()
        return test_user

def test_reports_page_load(client, app, setup_super_user):
    """
    Teszteli, hogy a /reports oldal sikeresen betölt-e egy bejelentkezett szuperfelhasználónak.
    """
    with app.test_request_context():
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        response = client.get(url_for('reports'))
        assert response.status_code == 200
        assert b'Riportok' in response.data or b'reports' in response.data.lower()

def test_reports_filter_post(client, app, setup_super_user):
    """
    Teszteli a riportok szűrését különböző szempontok szerint.
    """
    with app.test_request_context():
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        # Teszteljük a különböző csoportosítási szempontokat
        group_criteria = ['defect_type', 'customer', 'product', 'status', 'department', 'monthly_cost', 'monthly_count']
        
        for criterion in group_criteria:
            # A 'monthly_cost' és 'monthly_count' a 'to_char' SQL függvényt használja,
            # ami SQLite-ban (tesztkörnyezet) nem létezik alapértelmezés szerint.
            if criterion in ['monthly_cost', 'monthly_count']:
                continue
                
            response = client.post(url_for('reports'), data={
                'start_date': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'end_date': date.today().strftime('%Y-%m-%d'),
                'group_by': criterion,
                'chart_type': 'bar'
            })
            assert response.status_code == 200
            # Ellenőrizzük, hogy a válasz tartalmaz-e grafikon adatokat (Chart.js-hez átadott változók)
            assert b'labels' in response.data.lower()
            assert b'values' in response.data.lower()

def test_pdf_generation_endpoint(client, app, setup_super_user):
    """
    Teszteli a PDF generáló végpontot.
    """
    with app.test_request_context():
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        # Biztosítsunk adatot a PDF-hez
        from application import db
        if not Reklamacio.query.first():
            # Conftest alapértelmezett adatai alapján hozzunk létre egyet ha nincs
            customer = Customer.query.first()
            product = Product.query.first()
            defect = DefectType.query.first()
            dept = Department.query.first()
            status = Status.query.first()
            user = User.query.first()
            
            rekl = Reklamacio(
                complaint_date=date.today(),
                complaint_number="TEST-PDF-001",
                product_identifier="PROD-001",
                quantity=1,
                user=user,
                customer=customer,
                product=product,
                defect_type=defect,
                department=dept,
                status=status
            )
            db.session.add(rekl)
            db.session.commit()

        response = client.post(url_for('download_report_pdf'), data={
            'start_date': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': date.today().strftime('%Y-%m-%d'),
            'group_by': 'defect_type',
            'chart_type': 'bar'
        })
        
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/pdf'

@patch('application.utils.email_service.send_report_email')
def test_reports_send_email_post(mock_send_email, client, app, setup_super_user):
    """
    Teszteli a riport e-mailben történő elküldését (mockolt e-mail küldéssel).
    """
    mock_send_email.return_value = True
    
    with app.test_request_context():
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        response = client.post(url_for('send_report_email_route'), data={
            'recipient_email': 'recipient@example.com',
            'start_date': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': date.today().strftime('%Y-%m-%d'),
            'group_by': 'defect_type',
            'chart_type': 'bar'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Ha nincs adat, figyelmeztetést kapunk, ha van, akkor sikeres küldést
        assert b'adat' in response.data or b'sikeresen' in response.data.lower()

def test_reports_access_control(client, app):
    """
    Teszteli, hogy egy sima felhasználó nem fér hozzá a riportokhoz.
    """
    with app.test_request_context():
        # Állítsuk a teszt felhasználót 'user' role-ra
        from application import db
        user_role = Role.query.filter_by(name='user').first()
        test_user = User.query.filter_by(username='tesztelek').first()
        test_user.role_id = user_role.id
        db.session.commit()
        
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        response = client.get(url_for('reports'))
        # Átirányítás vagy hiba (roles_required dekorátor szerint)
        assert response.status_code in [302, 403]

def test_reports_empty_data(client, app, setup_super_user):
    """
    Teszteli a riport generálást olyan időszakra, ahol nincs adat.
    """
    with app.test_request_context():
        client.post(url_for('login'), data={'email': 'teszt@example.com', 'password': 'OldPassword1!'})
        
        # Jövőbeli dátum, valószínűleg nincs adat
        future_date = (date.today() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        response = client.post(url_for('download_report_pdf'), data={
            'start_date': future_date,
            'end_date': future_date,
            'group_by': 'defect_type',
            'chart_type': 'bar'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Nincs adat' in response.data
