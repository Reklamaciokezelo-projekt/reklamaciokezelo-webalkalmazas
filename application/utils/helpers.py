import re
import unicodedata
from application import db
from sqlalchemy import func, extract
from datetime import datetime, date
from application.models import Reklamacio, Status, Department


# --- Hónap nevek ---
HONAPOK_TELJES = ['Január', 'Február', 'Március', 'Április', 'Május', 'Június', 
                  'Július', 'Augusztus', 'Szeptember', 'Október', 'November', 'December']


# ----------------------------------------------------------------------
# Adatok tisztítása
# ----------------------------------------------------------------------
def slugify(text):
    """
    Bevitt adatok teljes tisztítás (ékezetek, speckarakterek, szóközök)
    """
    if not text:
        return ""
    # -- Ékezetek eltávolítása --
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # -- Kisbetű és felesleges szóközök levágása a szélekről --
    text = text.lower().strip()
    # -- Minden törlése, ami nem betű vagy szám (speciális karakterek és szóközök) --
    text = re.sub(r'[^a-z0-9]', '', text)
    
    return text

    
# ----------------------------------------------------------------------
# Adatbeviteli segédfüggvény: listaelem kiválasztása vagy új rekord létrehozása
# ----------------------------------------------------------------------
def get_or_create_dynamic(model, input_value):
    """
    Megkeresi a meglévő rekordot ID alapján,
    vagy új objektumot készít, ha az érték 'NEW_' prefixszel érkezik.
    """
    if not input_value:
        return None
    
    # --- Új rekord létrehozása (frontend 'NEW_' prefix alapján) ---
    if input_value.startswith('NEW_'):

        # --- Prefix eltávolítása ---
        new_display_name = input_value[4:].strip()
        
        if not new_display_name:
            return None
        
        # --- Belső (slug) név generálása ---
        internal_name = slugify(new_display_name)
        
        # --- Duplikáció ellenőrzése név alapján ---
        obj = model.query.filter_by(name=internal_name).first()
        
        # --- Ha nem létezik, új objektum előkészítése ---
        if not obj:
            obj = model(name=internal_name, display_name=new_display_name)
            db.session.add(obj)
            
        return obj

    # --- Meglévő rekord lekérése ID alapján ---
    else:
        try:
            obj_id = int(input_value)
            return model.query.get(obj_id)
        except (ValueError, TypeError):
            return None
    

# ----------------------------------------------------------------------
# Dashboard segédfüggvény: 
# ----------------------------------------------------------------------
def get_dashboard_stats():

    now = datetime.now()
    EXCLUDED_STATUS_NAME = 'visszautasitva'

    # ----------------------------------------------------------------------
    # Dashboard Kártyák
    # ----------------------------------------------------------------------
    # --- 1.Kártya / Aktuális havi reklamációk darabszámának lekérdezése ---
    count = Reklamacio.query.join(Status).filter(
        extract('year', Reklamacio.complaint_date) == now.year,
        extract('month', Reklamacio.complaint_date) == now.month,
        Status.name != EXCLUDED_STATUS_NAME
    ).count()

    # --- 2.Kártya / Aktuális havi reklamációs költségek összesítése ---
    cost_result = db.session.query(func.sum(Reklamacio.total_cost))\
        .join(Status)\
        .filter(
            extract('year', Reklamacio.complaint_date) == now.year,
            extract('month', Reklamacio.complaint_date) == now.month,
            Status.name != EXCLUDED_STATUS_NAME
        ).scalar()
    
    # --- None kezelése (None -> 0) ---
    cost = cost_result if cost_result else 0

    # --- 3.Kártya / Éves összesített költség ---
    year_cost_result = db.session.query(func.sum(Reklamacio.total_cost))\
        .join(Status)\
        .filter(
            extract('year', Reklamacio.complaint_date) == now.year,
            Status.name != EXCLUDED_STATUS_NAME
        ).scalar()
    
    # --- None kezelése (None -> 0) ---
    year_cost = year_cost_result if year_cost_result else 0

    # --- 4.Kártya / Éves visszaszállítást igénylő reklamációk száma ---
    return_count = Reklamacio.query.join(Status).filter(
        extract('year', Reklamacio.complaint_date) == now.year,
        Status.name != EXCLUDED_STATUS_NAME,
        Reklamacio.requires_return == True
    ).count()
    
    # ----------------------------------------------------------------------
    # Reklamáció oszlop grafikon
    # ----------------------------------------------------------------------
    # --- Időtengely előkészítése (Gördülő 12 hónap) ---
    labels = []
    counts = [0] * 12
    year_months = []

    # --- Dátumválasztó (év) ---
    year_change_index = -1 
    curr_y = now.year
    curr_m = now.month

    # --- Ciklus az elmúlt 12 hónap listájához (visszafelé 11-től 0-ig) ---
    for i in range(11, -1, -1):
        m = curr_m - i
        y = curr_y
        if m <= 0:
            m += 12
            y -= 1

        year_months.append((y, m))
        labels.append(HONAPOK_TELJES[m - 1])
        
        # --- Ha a hónap Január, és nem az utolsó (aktuális) hónap, akkor index mentése ---
        if m == 1 and i < 11:
            year_change_index = 11 - i

    # --- A kezdő dátum a legelső vizsgált hónap 1. napja ---
    start_date = date(year_months[0][0], year_months[0][1], 1)
    
    # --- Adatok lekérdezése a kezdő dátumtól ---
    monthly_counts = db.session.query(
        extract('year', Reklamacio.complaint_date).label('year'),
        extract('month', Reklamacio.complaint_date).label('month'),
        func.count(Reklamacio.id)
    ).join(Status).filter(
        Reklamacio.complaint_date >= start_date,
        Status.name != EXCLUDED_STATUS_NAME
    ).group_by('year', 'month').all()

    # --- A lekérdezett számok elhelyezése a megfelelő oszlopba ---
    for y, m, count_val in monthly_counts:
        try:
            idx = year_months.index((int(y), int(m)))
            counts[idx] = count_val
        except ValueError:
            # --- Ha valamiért kilógna az adat, átugrás ---
            pass

    # --- Adatok becsomagolása a grafikonnak ---
    monthly_data = {
        'labels': labels,
        'counts': counts,
        'year_change_index': year_change_index
    }

    # ----------------------------------------------------------------------
    # Üzemegység kártya
    # ----------------------------------------------------------------------
    dept_query = db.session.query(
        Department.display_name, 
        func.count(Reklamacio.id)
    ).select_from(Reklamacio)\
     .join(Department)\
     .join(Status)\
     .filter(
        extract('year', Reklamacio.complaint_date) == now.year,
        Status.name != EXCLUDED_STATUS_NAME
    ).group_by(Department.display_name)\
     .order_by(func.count(Reklamacio.id).desc()).all()

    # --- Szótár list létrehozása ---
    dept_data = [{'name': dept_name, 'count': count} for dept_name, count in dept_query]

    # --- Visszatérési értékek ---
    return count, cost, year_cost, return_count, monthly_data, dept_data