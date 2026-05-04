# --- Alap képfájl meghatározása ---
FROM python:3.12-slim

# ---Környezeti változók beállítása ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=application


WORKDIR /app

# --- Függőségek telepítése ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Alkalmazáskód és konfigurációs fájlok átmásolása ---
COPY config.py ./
COPY application ./application
COPY migrations ./migrations

# --- Indító szkript (entrypoint) átmásolása ---
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# --- Biztonsági beállítások ---
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app \
    && chown appuser:appuser /docker-entrypoint.sh
USER appuser

# --- Az alkalmazás által használt port deklarálása ---
EXPOSE 8000

# --- A konténer indulásakor lefutó szkript kijelölése ---
ENTRYPOINT ["/docker-entrypoint.sh"]
