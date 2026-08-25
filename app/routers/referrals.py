from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.enums import ReferralListingStatus
from app.models.referral import Referral
from app.models.user import User
from app.schemas import ReferralCreate, ReferralOut, ReferralSearch, ReferralUpdate
from app.services.ai_service import parse_job_description

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.post("", response_model=ReferralOut, status_code=201)
def create_referral(
    payload: ReferralCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.active_role.value != "referrer" and user.role.value not in ("referrer", "both"):
        raise HTTPException(status_code=403, detail="Switch to referrer role to create referrals")
    referral = Referral(
        referrer_id=user.id,
        company=payload.company,
        job_title=payload.job_title,
        job_link=payload.job_link,
        job_id=payload.job_id,
        job_description=payload.job_description,
        referral_deadline=payload.referral_deadline,
        slots=payload.slots,
    )
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return referral


@router.post("/{referral_id}/parse", response_model=ReferralOut)
def parse_referral(referral_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    referral = db.get(Referral, referral_id)
    if not referral or referral.referrer_id != user.id:
        raise HTTPException(status_code=404, detail="Referral not found")
    parsed = parse_job_description(referral.job_description, referral.job_title)
    referral.parsed_role = parsed.parsed_role
    referral.parsed_experience = parsed.parsed_experience
    referral.required_skills = parsed.required_skills
    referral.preferred_skills = parsed.preferred_skills
    referral.education_required = parsed.education_required
    referral.certifications_required = parsed.certifications_required
    referral.visa_sponsorship = parsed.visa_sponsorship
    referral.location = parsed.location
    referral.remote_ok = parsed.remote_ok
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return referral


@router.put("/{referral_id}", response_model=ReferralOut)
def update_referral(
    referral_id: int,
    payload: ReferralUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    referral = db.get(Referral, referral_id)
    if not referral or referral.referrer_id != user.id:
        raise HTTPException(status_code=404, detail="Referral not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(referral, field, value)
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return referral


@router.post("/{referral_id}/publish", response_model=ReferralOut)
def publish_referral(referral_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    referral = db.get(Referral, referral_id)
    if not referral or referral.referrer_id != user.id:
        raise HTTPException(status_code=404, detail="Referral not found")
    referral.status = ReferralListingStatus.PUBLISHED
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return referral


@router.get("/mine", response_model=list[ReferralOut])
def my_referrals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Referral).filter(Referral.referrer_id == user.id).order_by(Referral.created_at.desc()).all()


@router.get("/search", response_model=list[ReferralOut])
def search_referrals(
    company: str | None = Query(default=None),
    role: str | None = Query(default=None),
    technology: str | None = Query(default=None),
    location: str | None = Query(default=None),
    remote: bool | None = Query(default=None),
    visa_sponsorship: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Referral).filter(Referral.status == ReferralListingStatus.PUBLISHED)
    if company:
        query = query.filter(Referral.company.ilike(f"%{company}%"))
    if role:
        query = query.filter(or_(Referral.job_title.ilike(f"%{role}%"), Referral.parsed_role.ilike(f"%{role}%")))
    if technology:
        query = query.filter(
            or_(
                Referral.required_skills.ilike(f"%{technology}%"),
                Referral.preferred_skills.ilike(f"%{technology}%"),
                Referral.job_description.ilike(f"%{technology}%"),
            )
        )
    if location:
        query = query.filter(Referral.location.ilike(f"%{location}%"))
    if remote is not None:
        query = query.filter(Referral.remote_ok == remote)
    if visa_sponsorship is not None:
        query = query.filter(Referral.visa_sponsorship == visa_sponsorship)
    return query.order_by(Referral.created_at.desc()).all()


@router.get("/{referral_id}", response_model=ReferralOut)
def get_referral(referral_id: int, db: Session = Depends(get_db)):
    referral = db.get(Referral, referral_id)
    if not referral or referral.status != ReferralListingStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Referral not found")
    return referral


@router.get("/{referral_id}/recommendations", response_model=list[ReferralOut])
def recommend_referrals(referral_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Simple AI recommendation: return similar published referrals."""
    if not user.candidate_profile:
        return []
    target = db.get(Referral, referral_id)
    skills = (user.candidate_profile.skills or "").lower()
    query = db.query(Referral).filter(Referral.status == ReferralListingStatus.PUBLISHED)
    if target:
        query = query.filter(Referral.id != target.id)
    results = query.limit(20).all()
    if not skills:
        return results[:5]
    ranked = sorted(
        results,
        key=lambda r: sum(1 for word in skills.split(",") if word.strip() and word.strip() in (r.required_skills or "").lower()),
        reverse=True,
    )
    return ranked[:5]
