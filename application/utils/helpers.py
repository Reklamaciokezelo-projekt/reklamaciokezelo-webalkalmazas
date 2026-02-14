import re
import unicodedata
from application import db


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
    vagy új objektumot készít szöveges bevitel esetén.
    """
    if not input_value:
        return None
    
    try:
        # --- Szám esetén: meglévő rekord lekérése ID alapján ---
        obj_id = int(input_value)
        return model.query.get(obj_id)
    except (ValueError, TypeError):
        # --- Szöveg esetén: új érték feldolgozása ---
        new_display_name = input_value.strip()
        internal_name = slugify(new_display_name)
        
        # --- Ellenőrzés: létezik-e már ilyen rekord ---
        obj = model.query.filter_by(name=internal_name).first()
        
        if not obj:
            # --- Új rekord előkészítése (commit nélkül) ---
            obj = model(name=internal_name, display_name=new_display_name)
            db.session.add(obj)
        
        return obj