import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config import settings


def send_waitlist_confirmation(to_email: str, name: str, confirmation_url: str | None = None) -> bool:
    """Send a confirmation email to the waitlist registrant.

    If confirmation_url is provided, include it as an HTML link. Returns True if the email was sent successfully; False if SMTP not configured or send failed.
    """
    if not settings.smtp_host or not settings.smtp_from:
        # SMTP not configured; skip sending
        return False

    msg = EmailMessage()
    msg["Subject"] = "You're on the Reffery waitlist — confirm your email"
    msg["From"] = settings.smtp_from
    msg["To"] = to_email

    text_body = f"Hi {name},\n\nThanks for joining the Reffery waitlist. Please confirm your email by visiting the link below:\n\n{confirmation_url or '(confirmation link)'}\n\n— The Reffery Team"
    msg.set_content(text_body)

    if confirmation_url:
        html_body = f"<html><body><p>Hi {name},</p><p>Thanks for joining the Reffery waitlist. Please confirm your email by clicking the button below:</p><p><a href=\"{confirmation_url}\" style=\"display:inline-block;padding:12px 18px;background:#d97706;color:#fff;border-radius:6px;text-decoration:none\">Confirm my email</a></p><p>— The Reffery Team</p></body></html>"
        msg.add_alternative(html_body, subtype='html')

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
    except Exception as e:
        # swallow exceptions and return False — caller will record failure
        # Log the exception for debugging
        try:
            print(f"email send failed: {e}")
        except Exception:
            pass
        return False
