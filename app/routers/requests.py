from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.enums import Availability, NotificationType, ReferralRequestStatus
from app.models.referral import Referral, ReferralRequest
from app.models.user import User
from app.schemas import ReferralRequestCreate, ReferralRequestOut, ReviewDecision, StatusUpdate
from app.services.ai_service import evaluate_match
from app.services.notification_service import create_notification
from app.services.referral_status_service import validate_status_transition
from app.services.reputation_service import add_reputation

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/referrals/{referral_id}", response_model=ReferralRequestOut, status_code=201)
def request_referral(
    referral_id: int,
    payload: ReferralRequestCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.availability.value == "not_looking":
        raise HTTPException(status_code=400, detail="Your availability is set to Not Looking")
    if not user.candidate_profile:
        raise HTTPException(status_code=400, detail="Complete your candidate profile first")
    referral = db.get(Referral, referral_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    if referral.slots_filled >= referral.slots:
        raise HTTPException(status_code=400, detail="No referral slots available")

    evaluation = evaluate_match(user.candidate_profile, referral)
    req = ReferralRequest(
        referral_id=referral.id,
        candidate_id=user.id,
        resume_version=payload.resume_version or user.candidate_profile.resume_text,
        portfolio_url=payload.portfolio_url or user.candidate_profile.portfolio_url,
        cover_message=payload.cover_message,
        match_score=evaluation.match_score,
        match_explanation=evaluation.match_explanation,
        strengths=evaluation.strengths,
        missing_skills=evaluation.missing_skills,
        ai_recommendation=evaluation.ai_recommendation,
    )
    db.add(req)
    referrer = db.get(User, referral.referrer_id)
    if referrer:
        create_notification(
            db,
            referrer,
            NotificationType.GENERAL,
            "New Referral Request",
            f"{user.name} requested a referral for {referral.job_title} at {referral.company}.",
        )
    db.commit()
    db.refresh(req)
    return req


@router.get("/mine", response_model=list[ReferralRequestOut])
def my_requests(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ReferralRequest).filter(ReferralRequest.candidate_id == user.id).all()


@router.get("/incoming", response_model=list[ReferralRequestOut])
def incoming_requests(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    referral_ids = [r.id for r in user.referrals_posted]
    if not referral_ids:
        return []
    return db.query(ReferralRequest).filter(ReferralRequest.referral_id.in_(referral_ids)).all()


@router.get("/{request_id}", response_model=ReferralRequestOut)
def get_request(request_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    req = db.get(ReferralRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    referral = db.get(Referral, req.referral_id)
    if req.candidate_id != user.id and referral.referrer_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return req


@router.post("/{request_id}/review", response_model=ReferralRequestOut)
def review_request(
    request_id: int,
    decision: ReviewDecision,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    req = db.get(ReferralRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    referral = db.get(Referral, req.referral_id)
    if referral.referrer_id != user.id:
        raise HTTPException(status_code=403, detail="Only the referrer can review")
    if req.status != ReferralRequestStatus.REQUESTED:
        raise HTTPException(status_code=400, detail="Request already reviewed")

    candidate = db.get(User, req.candidate_id)
    if decision.accept:
        req.status = ReferralRequestStatus.ACCEPTED
        referral.slots_filled += 1
        add_reputation(db, candidate, "referral_accepted", f"Accepted for {referral.job_title}")
        create_notification(
            db, candidate, NotificationType.REFERRAL_ACCEPTED,
            "Referral Accepted", f"Your referral request for {referral.job_title} was accepted.",
        )
    else:
        req.status = ReferralRequestStatus.REJECTED
        add_reputation(db, candidate, "referral_declined")
        create_notification(
            db, candidate, NotificationType.REFERRAL_DECLINED,
            "Referral Declined", f"Your referral request for {referral.job_title} was declined.",
        )
    db.add(req)
    db.add(referral)
    db.commit()
    db.refresh(req)
    return req


@router.patch("/{request_id}/status", response_model=ReferralRequestOut)
def update_status(
    request_id: int,
    payload: StatusUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    req = db.get(ReferralRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    referral = db.get(Referral, req.referral_id)
    if req.candidate_id != user.id and referral.referrer_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    validate_status_transition(req.status, payload.status)
    req.status = payload.status

    candidate = db.get(User, req.candidate_id)
    if payload.status == ReferralRequestStatus.SUBMITTED:
        add_reputation(db, candidate, "referral_submitted")
    if payload.status == ReferralRequestStatus.JOINED:
        add_reputation(db, candidate, "referral_joined")
        add_reputation(db, user, "successful_hire_referrer")
        candidate.availability = Availability.NOT_LOOKING

    create_notification(
        db, candidate, NotificationType.STATUS_UPDATE,
        "Referral Status Updated", f"Status is now: {payload.status.value.replace('_', ' ').title()}",
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.post("/{request_id}/mark-hired", response_model=ReferralRequestOut)
def mark_hired(request_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    req = db.get(ReferralRequest, request_id)
    if not req or req.candidate_id != user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = ReferralRequestStatus.JOINED
    user.availability = Availability.NOT_LOOKING
    add_reputation(db, user, "referral_joined", "Marked as hired")
    db.add(req)
    db.add(user)
    db.commit()
    db.refresh(req)
    return req
