from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime

from app.database import get_db
from app.models.waitlist import WaitlistEntry
from app.schemas import WaitlistCreate, WaitlistOut, WaitlistOutWithConfirm
from app.services.email_service import send_waitlist_confirmation
from app.config import settings

router = APIRouter(prefix="/waitlist", tags=["waitlist"])


def _make_token(entry_id: int, expires_hours: int = 72) -> str:
    payload = {"entry_id": entry_id, "exp": int((datetime.utcnow() + timedelta(hours=expires_hours)).timestamp())}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def _decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])


@router.post("", response_model=WaitlistOutWithConfirm, status_code=201)
def create_waitlist_entry(request: Request, payload: WaitlistCreate, db: Session = Depends(get_db)):
    # Basic duplicate check
    existing = db.query(WaitlistEntry).filter(WaitlistEntry.email == payload.email).first()
    if existing:
        # If already confirmed, return it; otherwise, generate a fresh confirmation link
        if existing.confirmed:
            return existing
        token = _make_token(existing.id)
        confirm_url = str(request.url_for("confirm_waitlist") + f"?token={token}")
        return {**existing.__dict__, "confirmed": existing.confirmed, "confirmation_url": confirm_url}

    entry = WaitlistEntry(name=payload.name.strip(), email=payload.email, role=payload.role or "both")
    db.add(entry)
    db.commit()
    db.refresh(entry)

    token = _make_token(entry.id)
    confirm_url = str(request.url_for("confirm_waitlist") + f"?token={token}")

    # Try to send confirmation email if SMTP configured
    sent = send_waitlist_confirmation(entry.email, entry.name, confirmation_url=confirm_url)
    if sent:
        # Do not mark confirmed until user clicks confirmation link
        pass
    else:
        # SMTP not configured — return the confirmation_url in response for testing
        print(f"Confirmation URL (dev): {confirm_url}")

    # Return entry and include confirmation_url when SMTP is not configured (or always for convenience)
    return {**entry.__dict__, "confirmed": entry.confirmed, "confirmation_url": confirm_url}


@router.get("/confirm")
def confirm_waitlist(token: str, db: Session = Depends(get_db)):
    try:
        data = _decode_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    entry_id = data.get("entry_id")
    if not entry_id:
        raise HTTPException(status_code=400, detail="Invalid token")
    entry = db.get(WaitlistEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Waitlist entry not found")
    if not entry.confirmed:
        entry.confirmed = True
        db.add(entry)
        db.commit()
        db.refresh(entry)
    return {"status": "confirmed", "email": entry.email}
