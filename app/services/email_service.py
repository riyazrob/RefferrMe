import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config import settings


def send_waitlist_confirmation(to_email: str, name: str) -> bool:
    """Send a simple confirmation email to the waitlist registrant.

    Returns True if the email was sent (or attempted) and False if SMTP not configured.
    """
    if not settings.smtp_host or not settings.smtp_from:
        # SMTP not configured; skip sending
        return False

    msg = EmailMessage()
    msg["Subject"] = "You're on the Reffery waitlist — thanks!"
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    body = f"Hi {name},\n\nThanks for joining the Reffery waitlist. We'll email you when we open the closed beta.\n\n— The Reffery Team"
    msg.set_content(body)

    host = settings.smtp_host
    port = settings.smtp_port or (465 if settings.smtp_tls else 25)

    try:
        if settings.smtp_tls and port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            if settings.smtp_tls:
                server.starttls()
        if settings.smtp_user and settings.smtp_password:
            server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        # swallow exceptions and return False — caller will record failure
        return False
