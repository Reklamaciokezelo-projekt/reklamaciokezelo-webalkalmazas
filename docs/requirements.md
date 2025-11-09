# Projekt Követelmények

## 1. Bevezetés
Ez a dokumentum tartalmazza a rendszerrel kapcsolatos követelményeket.  
- **A rendszer célja** - A vállalathoz beérkező reklamációk kezelése, tárolása, kimutatások és statisztikák készítése a felhasználó által kiválasztott kritériumok alapján

---

## 2. Funkcionális követelmények
A rendszernek biztosítania kell az alábbi funkciókat:

- **Regisztráció** - a felhasználó tud új fiókot létrehozni.**OK**
- **Bejelentkezés** - a felhasználó a regisztrált adataival be tud lépni.**OK** 
- **Felhasználói adatok módosítása** - a bejelentkezett felhasználó tudja módosítani az adatait.**OK**
- **Elfelejtett felhasználónév, vagy jelszó** - A felhasználó tudjon segítséget kérni bejelentkezési probléma esetén az adminisztrátoltól.
- **Felhasználói fiók törlése** - az adminisztrátor tudja törölni a felhasználó fiókját.**OK**
- **Adatkezelés** - a  bejelentkezett felhasználó tud adatokat rögzíteni, módosítani és törölni.  
- **Keresés** - a felhasználó tudjon adatokat keresni különböző feltételek alapján.  
- **Kimutatás készítés** - a felhasználó tudjon kimutatást készíteni a választott feltételek alapján.
- **Exportálás** - lehessen exportálni kimutatásokat (CSV, PDF).
- **Statisztikák** - havi hibaszázalék kimutatása.
- **Értesítések** - e-mail értesítés a regisztrált felhasználóknak új reklamációról (e-mail).
- **Jogosultságkezelés** - Különböző felhasználói szintek, különböző funkciók használatára jogosultak.

---

## 3. Nem funkcionális követelmények
A rendszer minőségi jellemzői:

- **Teljesítmény** - a rendszer átlagos válaszideje < 2 másodperc.  
- **Biztonság** - jelszavak titkosított tárolása, HTTPS kapcsolat.  
                - Brute force elleni védelem.
                - SQL injection elleni védelem.
- **Megbízhatóság** - a rendszer rendelkezésre állása legalább 99%.  
- **Használhatóság** - egyszerű, reszponzív webes felület. 
- **Skálázhatóság** - a rendszer legyen képes nagyobb adatmennyiséggel is megfelelően működni.
- **Karbantarthatóság** - a kód legyen átlátható, jól dokumentált.

---

## 4. User Story-k
Az alábbi user story-k mutatják be a felhasználói igényeket:

- **Felhasználóként szeretnék regisztrálni**, hogy saját fiókom legyen.  
- **Felhasználóként szeretnék bejelentkezni**, hogy hozzáférjek az adataimhoz és jogosult legyek adatok rögzítésére.  
- **Felhasználóként szeretnék segítséget kérni a bejelentkezéshez (Elfelejtett jelszó)**, hogy hozzáférjek az adataimhoz.  
- **Bejelentkezett felhasználóként szeretném megtekinteni a saját adataimat**, hogy ellenőrizhessem őket.  
- **Bejelentkezett felhasználóként szeretném módosítani a saját adataimat**, hogy az aktuális adatok szerepeljenek a fiókomban.  
- **Bejelentkezett felhasználóként szeretném törölni a fiókomat**, hogy a fiók megszűnjön.  
- **Felhasználóként keresek a reklamációs adatok között**, hogy megtaláljam a számomra releváns információt.
- **Felhasználóként szeretnék kimutatást készíteni a reklamációs adatokból**, hogy áttekinthető formában lássam az eredményeket.
- **Bejelentkezett felhasználóként szeretnék új reklamációt rögzíteni**, hogy a probléma hivatalosan nyilvántartásba kerüljön.
- **Bejelentkezett felhasználóként szeretnék reklamációt törölni/módosítani a rendszerben**, hogy az adatok naprakészek legyenek.
- **Adminisztrátorként szeretném törölni a felhasználókat**, hogy kezelni tudjam a jogosultságokat.  

---

## 5. Szerepkörök
| Szerep                      | Leírás                                                                                                                        |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Felhasználó                 | Alap funkciók használata (regisztráció, bejelentkezés, adatkeresés, kimutatás készítés).                                      |
| Bejelentkezett Felhasználó  | Alap funkciók használata (személyes adatok módosítása, adatkeresés, kimutatás készítés, adatok rögzítése/törlése/módosítása). |
| Admin                       | Felhasználók és jogosultságok kezelése.                                                                                       |

---

## 6. Technikai követelmények
- Backend: **Python Flask**  
- Adatbázis: **PostgreSQL**  
- Frontend: **HTML, CSS, Bootstrap**  
- Verziókezelés: **GitHub**  

---

## 7. Feltételezések
- A felhasználók rendelkeznek internetkapcsolattal és modern webböngészővel.  
- A szerver környezet biztosítja a Python 3.11 és PostgreSQL telepítését.  
- Az adminisztrátorok karbantartják a rendszer adatbázisát.  
- A felhasználók valós adatokat adnak meg regisztráció során.  

---

## 8. Kockázatok
- A rendszer teljesítménye romolhat, ha a felhasználói szám gyorsan megnő.  
- Biztonsági kockázatok (pl. SQL injection, brute force támadások).  
- A fejlesztés késhet, ha új követelmények jelennek meg.    
- Emberi tényező: a felhasználók rossz jelszót választanak, vagy elfelejtik azt.  

---
