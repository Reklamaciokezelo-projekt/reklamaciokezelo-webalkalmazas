# Reklamációkezelő webalkalmazás

Flask alapú reklamációkezelő. **Éles vagy személyes kiszolgálóra** elegendő előfeltétel: **Docker Engine** és **Docker Compose** (beleértve a `docker compose` parancsot). Nem szükséges telepíteni a Python futtatókörnyezetét, PostgreSQL klienst vagy egyéb eszközöket a gépre.

A Docker stack **nem** a projekt gyökerében lévő **`.env`** fájlt használja (a Compose alapértelmezés szerint megpróbálja betölteni, és Windowson ez gyakran hibás „mappa `.env`”, OneDrive vagy elérési út miatt). A generált és a Compose által használt fájl neve: **`docker.env`**.

## Előfeltételek

- **Docker Engine** (Linux, Docker Desktop macOS/Windows, vagy kompatibilis futtatókörnyezet).
- **Docker Compose plugin**, minimum **2.24-es** verzió vagy újabb. Indokok: a `service_completed_successfully` indulási feltétel **(2.20+)** az init → Postgres sorrendhez, valamint a **`env_file` / `required: false` (2.24+)** azért kell, hogy az első indításkor a **`docker.env` még ne létezzen** se hibát ne okozzon. Az első `docker compose up` után az `init-env` létrehozza a **`docker.env`** fájlt.

Ellenőrzés például:

```bash
docker compose version
```

## Első indítás (csak Docker)

1. Klónozd vagy csomagold ki a projektet, lépj a projekt gyökérkönyvtárába.

2. **Windows / Desktop / OneDrive:** Ha korábban volt hibás **`.env`** (fájl vagy mappa), töröld vagy nevezd át, különben a Compose megakadhat az olvasásán (`failed to read .env`, *Nem megfelelő funkció*). Lásd **[Windows és `.env`](#windows-és-env)** lent.

3. Indítsd a szolgáltatásokat:

   ```bash
   docker compose up -d --build
   ```

   **Első alkalommal** a következő történik:

   - **`init-env`**: ha még **nincs** `docker.env`, létrehozza **véletlenszerű értékekkel** (ugyanazok a kulcsok, mint a [docker.env.example](docker.env.example)-ben). Ha létezik **régi** `.env` **fájl** (nem mappa), de nincs `docker.env`, átmásolja `.env` → `docker.env` (átvitel).
   - **`db`**: a projekt mappa **read-only** be van kötve `/project` alá; indulás előtt a konténer **betölti** (`source`) a `/project/docker.env` fájlt — így a `POSTGRES_PASSWORD` Windowson is bejut (az `env_file` néha üresen hagyja). Adatok: `pgdata` kötet.
   - **`web`**: szintén látja a `/project/docker.env` fájlt ([`config.py`](config.py)); migráció (`flask db upgrade`), majd Gunicorn.

4. **Megnyitás:** `http://localhost:8000` (vagy `WEB_PORT` a `docker.env`-ben; az első indításkor a host portot a Compose alapból **8000**-ra veszi — lásd lent).

### `WEB_PORT` és a Compose

A `${WEB_PORT:-8000}` interpoláció a **shell** vagy egy opcionális **projekt `.env`** fájlból jön; a stack szándékosan **`docker.env`**-et használ, hogy elkerülje a Windowos `.env` gondokat. Ezért:

- Alapértelmezés: host port **8000**.
- Más porthoz: indítsd így (PowerShell: `$env:WEB_PORT=9000`), vagy első indulás után állítsd a `docker.env`-ben a `WEB_PORT` értékét **és** futtasd:  
  `docker compose --env-file docker.env up -d --build`

### Meglévő `docker.env` nélküli klónozás

Nem kell `cp docker.env.example docker.env` az első alkalomhoz. Az első `docker compose up` előállítja a `docker.env` fájlt (írási jog a projekt mappájára a bind mounthoz kell).

## Windows és `.env` / `docker.env`

### `.env` (Compose automatikus betöltése)

A Docker Compose **automatikusan** megpróbálja beolvasni a projekt gyökerében lévő **`.env`** fájlt (változó-interpolációhoz). Ha **`.env` egy mappa**, **üres / hibás**, vagy az elérési út (Desktop, OneDrive, szinkron) miatt az olvasás elromlik, hibát kapsz, még mielőtt az `init-env` lefutna.

**Teendő:** töröld vagy nevezd át a **`.env`** nevű elemet (ha van). A stack környezeti fájlja: **`docker.env`**.

### `docker.env` lett **mappa** (nem fájl)

Ha a projekt mappában **`docker.env` egy könyvtár**, az tipikusan **Windows + Docker** mellékhatás: ha korábban (vagy más projektben) **fájlként** kötötték be a `./docker.env` útvonalat, de a fájl **még nem létezett**, a Docker Desktop gyakran **üres mappát** hoz létre `docker.env` néven. Ekkor az `init-env` nem tud normális fájlt írni.

**Teendő:**

1. Állítsd le: `docker compose down`
2. Töröld a **`docker.env` nevű mappát** (Windows Intéző, vagy PowerShell: `Remove-Item -Recurse -Force docker.env`)
3. Indíts újra: `docker compose up -d --build`

A jelenlegi `docker-compose.yml` **nem** köti be külön a `docker.env` fájlt (mappa-probléma Windowson) — a teljes projekt könyvtár **`/project`** alá kerül, onnan olvassuk a `docker.env`-et.

### Git Bash vs PowerShell

A **Docker Desktop** parancsai általában **mindkettőben** működnek. Ha Git Bash furcsa útvonalakat ad (pl. MSYS), próbáld **PowerShell**-ből vagy **CMD**-ből, ugyanabból a mappából: `docker compose up -d --build`. A projekt legyen lehetőleg **rövid, helyi** útvonalon (pl. `C:\dev\...`), ne OneDrive-Desktopon.

## Újratelepítés, `docker.env` és adatbázis kötet

- A **Postgres jelszó** **első** inicializáláskor kerül az adatkönyvtárba (`pgdata`). Később a `.env` / `docker.env` új jelszava **nem** írja felül automatikusan a kötetet. Ha **`password authentication failed for user "reklamacio_kezelo"`** jelenik meg: tipikusan új `docker.env` + régi `pgdata`.

  ```bash
  docker compose down -v
  rm -f docker.env
  docker compose up -d --build
  ```

  Windows: ha `docker.env` **fájl**, `del docker.env` (CMD) vagy `Remove-Item docker.env` (PowerShell). Ha **mappa** volt: `Remove-Item -Recurse -Force docker.env`.

  (`-v` törli a `pgdata` kötetet is; **adatvesztés**.)

- **Kézi `docker.env`:** `cp docker.env.example docker.env` (vagy másolás Windows Explorerrel), töltsd ki, majd `docker compose up`.

## Hiba elhárítás

| Tünet | Valószínű ok | Teendő |
|--------|----------------|--------|
| `failed to read ...\.env` / *Nem megfelelő funkció* (Windows) | A **`.env`** nem normál szövegfájl (mappa, OneDrive, elérési út) vagy a Compose nem tudja olvasni | Töröld / nevezd át a projekt gyökerében lévő **`.env`** elemet. Lásd **Windows és `.env` / `docker.env`**. |
| `docker.env` is a **folder** | Korábbi fájl-bind mount Windowson létrehozta a mappát | Töröld a **`docker.env` mappát**, `docker compose up` újra. Részletek: **Windows** szakasz. |
| `env file ... not found` (régi) | Régi Compose | Frissíts **2.24+**-ra. A `docker.env` **`required: false`**. |
| `Database is uninitialized...` / `db: ERROR: POSTGRES_PASSWORD is empty` | **`POSTGRES_PASSWORD`** nem került környezetbe (üres sor, **CRLF** (Windows) szerkesztés, vagy csak **`DATABASE_URL`** van kitöltve) | A `db` indulás előtt **levágja a sorvégi `\r`-t**, és ha kell, a **`DATABASE_URL`**-ből számolja a jelszót. Mentsd `docker.env`-et **UTF-8 LF**-fel, vagy **Újratelepítés**: `down -v`, töröld `docker.env`, `up`. |
| Flask „Could not locate application” / „No such command ‘db’” | `FLASK_APP` / környezet | `docker compose exec web env` — legyen `FLASK_APP=application`. `docker compose up -d --build web`. |
| `FATAL: role "root" does not exist` (db napló) | Ritkább a jelenlegi compose-szal | `docker compose up -d --force-recreate db`. |

**Megjegyzés:** A `db` és `web` szolgáltatás a projekt gyökerét **`/project:ro`** módon köti be. A Postgres belépési pont **`source /project/docker.env`** után indul — nem csak az `env_file`-ra támaszkodunk (Windows-kompatibilitás).

**Általános:** `docker compose version` (≥ 2.24), `docker compose config`. **Tiszta** újraindítás: fent az **Újratelepítés** szakasz.

## Migrációk

A **web** konténer induláskor **`flask db upgrade`**-et futtat. Külön parancs:

```bash
docker compose run --rm web flask db upgrade
```

## Resend e-mail (opcionális)

Az alkalmazás **Resend**-et használhat ([config.py](config.py)). A generált **`docker.env`**-ben ezek üresen maradhatnak. Kitöltés után indítsd újra a **web** szolgáltatást.

## HTTPS és reverse proxy (opcionális)

Éles domainhez **Caddy** vagy **nginx** proxy: cél `127.0.0.1:8000` (vagy a választott `WEB_PORT`).

## Adatmentés

Postgres adatok a **`pgdata`** kötetben. Ajánlott `pg_dump` vagy kötet-backup.

## Fejlesztés forráskódból

Lokális Python: [.env.example](.env.example); változók listája: [docker.env.example](docker.env.example). A [config.py](config.py) először a **`docker.env`**-et, majd a **`.env`** fájlt tölti be (ha létezik).
