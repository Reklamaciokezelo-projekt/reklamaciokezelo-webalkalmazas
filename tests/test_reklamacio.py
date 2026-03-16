import pytest
from flask import url_for
from application.models import Reklamacio, Customer, Product, DefectType, Department, Status

def test_create_reklamacio_get(client, app):
    """
    Teszteli, hogy az új reklamáció oldal betölt-e (GET kérés).
    Be kell hozzá lenni jelentkezve.
    """
    with app.test_request_context():
        # super_user role beállítása
        from application import db
        from application.models import Role, User
        super_role = Role.query.filter_by(name='super_user').first()
        if not super_role:
            super_role = Role(name='super_user', display_name='Szuperfelhasználó')
            db.session.add(super_role)
            db.session.commit()
            
        test_user = User.query.filter_by(username='tesztelek').first()
        test_user.role_id = super_role.id
        db.session.commit()

        # Bejelentkezés
        client.post(url_for('login'), data={
            'email': 'teszt@example.com',
            'password': 'OldPassword1!'
        })
        
        # GET kérés az új reklamáció oldalra
        response = client.get(url_for('uj_reklamacio'))
        assert response.status_code == 200
        assert 'reklam' in response.data.decode('utf-8').lower()

def test_create_reklamacio_post_success(client, app):
    """
    Teszteli egy új reklamáció felvételét (POST kérés űrlap adatokkal).
    """
    with app.test_request_context():
        from application import db
        from application.models import Role, User
        super_role = Role.query.filter_by(name='super_user').first()
        test_user = User.query.filter_by(username='tesztelek').first()
        test_user.role_id = super_role.id
        db.session.commit()

        # Bejelentkezés
        client.post(url_for('login'), data={
            'email': 'teszt@example.com',
            'password': 'OldPassword1!'
        })

        # Szükséges ID-k kinyerése a DB-ből (conftest.py _seed_test_data() hozta létre őket)
        customer = Customer.query.first()
        product = Product.query.first()
        defect = DefectType.query.first()
        dept = Department.query.first()
        status = Status.query.first()

        # POST kérés az adatokkal
        response = client.post(url_for('uj_reklamacio'), data={
            'complaint_date': '2025-10-10',
            'complaint_number': 'REK-TEST-001',
            'product_identifier': 'PID-12345',
            'customer': customer.id,
            'product': product.id,
            'defect_type': defect.id,
            'quantity': 10,
            'description': 'Teszt hiba leírása',
            'shipping_date': '2025-10-09',
            'requires_return': 'y',  # Boolean field checkbox
            'department': dept.id,
            'status': status.id,
            'total_cost': 5000,
            'submit': True
        }, follow_redirects=True)

        # Ellenőrizzük, hogy sikeresen létrejött-e
        assert response.status_code == 200
        response_text = response.data.decode('utf-8')
        assert 'Sikeresen' in response_text or 'reklamaciok' in response.request.path.lower()
        
        # Ellenőrizzük az adatbázisban
        new_rekl = Reklamacio.query.filter_by(complaint_number='REK-TEST-001').first()
        assert new_rekl is not None
        assert new_rekl.customer_id == customer.id
        # Ellenőrizzük a generált mezőket (pl. Reklamáció száma)
        assert new_rekl.complaint_number == 'REK-TEST-001'
        assert "REK" in new_rekl.complaint_number
