from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.waitlist import WaitlistEntry
from app.schemas import WaitlistCreate, WaitlistOut
from app.services.email_service import send_waitlist_confirmation

router = APIRouter(prefix="/waitlist", tags=["waitlist"])


@router.post("", response_model=WaitlistOut, status_code=201)
def create_waitlist_entry(payload: WaitlistCreate, db: Session = Depends(get_db)):
    # Basic duplicate check
    existing = db.query(WaitlistEntry).filter(WaitlistEntry.email == payload.email).first()
    if existing:
        # Return existing entry
        return existing

    entry = WaitlistEntry(name=payload.name.strip(), email=payload.email, role=payload.role or "both")
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # Try to send confirmation email if SMTP configured
    sent = send_waitlist_confirmation(entry.email, entry.name)
    if sent:
        entry.confirmed = True
        db.add(entry)
        db.commit()
        db.refresh(entry)

    return entry
