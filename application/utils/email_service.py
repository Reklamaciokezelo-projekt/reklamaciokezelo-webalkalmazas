import resend
from flask import current_app, url_for, render_template
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import base64


# ----------------------------------------------------------------------
# SEGÉDFÜGGVÉNYEK – TOKEN GENERÁLÁS ÉS ELLENŐRZÉS
# ----------------------------------------------------------------------

def _get_serializer():
    """Aláírt URL-token generátort ad vissza a SECRET_KEY alapján."""
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def generate_reset_token(email: str) -> str:
    """Aláírt, időkorlátozott jelszó-visszaállítási tokent generál az e-mail cím alapján."""
    s = _get_serializer()
    return s.dumps(email, salt='password-reset-salt')


def verify_reset_token(token: str):
    """
    Ellenőrzi a jelszó-visszaállítási tokent.
    Sikeres ellenőrzés esetén visszaadja az e-mail címet, hiba esetén None-t.
    """
    s = _get_serializer()
    expiry = current_app.config.get('PASSWORD_RESET_TOKEN_EXPIRY', 3600)
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiry)
    except (SignatureExpired, BadSignature):
        return None
    return email


# ----------------------------------------------------------------------
# JELSZÓ-VISSZAÁLLÍTÁSI E-MAIL KÜLDÉS
# ----------------------------------------------------------------------

def send_password_reset_email(user) -> bool:
    """
    Jelszó-visszaállítási e-mailt küld a megadott felhasználónak.
    A token az e-mail cím alapján generálódik, 1 óráig érvényes.
    Visszatérési értéke True siker esetén, False hiba esetén.
    """
    token = generate_reset_token(user.email)
    reset_url = url_for('reset_password', token=token, _external=True)

    html_body = render_template(
        'email/password_reset.html',
        user=user,
        reset_url=reset_url
    )

    resend.api_key = current_app.config['RESEND_API_KEY']

    try:
        resend.Emails.send({
            "from": current_app.config['MAIL_FROM'],
            "to": user.email,
            "subject": "Jelszó visszaállítása – Reklamációkezelő",
            "html": html_body,
        })
        return True
    except Exception as e:
        current_app.logger.error(f"E-mail küldési hiba (jelszó-visszaállítás, {user.email}): {e}")
        return False


# ----------------------------------------------------------------------
# RIPORT E-MAIL KÜLDÉS (PDF melléklettel)
# ----------------------------------------------------------------------

def send_report_email(to_email: str, pdf_buffer, filename: str, title_suffix: str, date_range: str) -> bool:
    """
    Riportot tartalmazó PDF-et küld e-mail mellékletként a megadott címre.
    Visszatérési értéke True siker esetén, False hiba esetén.
    """
    resend.api_key = current_app.config['RESEND_API_KEY']

    # --- PDF buffer base64 kódolása a Resend API számára ---
    pdf_buffer.seek(0)
    pdf_b64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')

    subject = f"Reklamációs riport – {title_suffix} ({date_range})"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0d6efd;">Reklamációkezelő – Riport</h2>
        <p>Csatolva találja a(z) <strong>{title_suffix}</strong> riportot a(z) <strong>{date_range}</strong> időszakra.</p>
        <p style="color: #888; font-size: 12px;">Ez egy automatikusan generált levél, kérjük ne válaszoljon rá.</p>
    </body>
    </html>
    """

    try:
        resend.Emails.send({
            "from": current_app.config['MAIL_FROM'],
            "to": to_email,
            "subject": subject,
            "html": html_body,
            "attachments": [
                {
                    "filename": filename,
                    "content": pdf_b64,
                }
            ],
        })
        return True
    except Exception as e:
        current_app.logger.error(f"E-mail küldési hiba (riport, {to_email}): {e}")
        return False


# ----------------------------------------------------------------------
# REKLAMÁCIÓ ÉRTESÍTŐ E-MAIL
# ----------------------------------------------------------------------

def send_reklamacio_notification_email(action: str, reklamacio) -> bool:
    """
    Értesítést küld egy reklamáció létrehozásáról, állapotváltozásáról vagy törléséről.
    Az értesítési címet a REKLAMACIOS_KOR_EMAIL konfig adja meg.
    """
    to_email = current_app.config.get('REKLAMACIOS_KOR_EMAIL')
    if not to_email:
        return False

    resend.api_key = current_app.config['RESEND_API_KEY']
    
    subject = f"{action} reklamáció: {reklamacio.complaint_number}"
    
    html_body = render_template(
        'email/reklamacio_notification.html',
        action=action,
        reklamacio=reklamacio
    )

    try:
        resend.Emails.send({
            "from": current_app.config['MAIL_FROM'],
            "to": to_email,
            "subject": subject,
            "html": html_body,
        })
        return True
    except Exception as e:
        current_app.logger.error(f"E-mail küldési hiba (reklamáció értesítés, {to_email}): {e}")
        return False

