from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.enums import EndorsementStatus
from app.models.endorsement import Endorsement
from app.models.user import User
from app.schemas import EndorsementCreate, EndorsementOut
from app.services.notification_service import create_notification
from app.services.reputation_service import add_reputation
from app.enums import NotificationType

router = APIRouter(prefix="/endorsements", tags=["endorsements"])


@router.post("", response_model=EndorsementOut, status_code=201)
def request_endorsement(
    payload: EndorsementCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.candidate_profile:
        raise HTTPException(status_code=400, detail="Candidate profile required")
    endorsement = Endorsement(
        candidate_profile_id=user.candidate_profile.id,
        endorser_name=payload.endorser_name,
        endorser_title=payload.endorser_title,
        endorser_email=payload.endorser_email,
        message=payload.message,
    )
    db.add(endorsement)
    db.commit()
    db.refresh(endorsement)
    return endorsement


@router.get("", response_model=list[EndorsementOut])
def list_endorsements(user: User = Depends(get_current_user)):
    if not user.candidate_profile:
        return []
    return user.candidate_profile.endorsements


@router.post("/{endorsement_id}/approve", response_model=EndorsementOut)
def approve_endorsement(endorsement_id: int, db: Session = Depends(get_db)):
    endorsement = db.get(Endorsement, endorsement_id)
    if not endorsement:
        raise HTTPException(status_code=404, detail="Endorsement not found")
    endorsement.status = EndorsementStatus.APPROVED
    candidate_user = endorsement.candidate_profile.user
    add_reputation(db, candidate_user, "endorsement_received", f"Endorsement from {endorsement.endorser_name}")
    create_notification(
        db,
        candidate_user,
        NotificationType.ENDORSEMENT,
        "New Endorsement",
        f"{endorsement.endorser_name} endorsed your profile.",
    )
    db.add(endorsement)
    db.commit()
    db.refresh(endorsement)
    return endorsement
