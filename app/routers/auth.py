from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.enums import ActiveRole, UserRole
from app.models.profile import CandidateProfile, ReferrerProfile
from app.models.user import User
from app.schemas import (
    ActiveRoleSwitch,
    CandidateProfileOut,
    CandidateProfileUpdate,
    ReferrerProfileOut,
    ReferrerProfileUpdate,
    RoleSelect,
    UserOut,
)
from app.services.ai_service import analyze_profile
from app.services.reputation_service import add_reputation

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/role", response_model=UserOut)
def select_role(payload: RoleSelect, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.role = payload.role
    if payload.role == UserRole.REFERRER:
        user.active_role = ActiveRole.REFERRER
    else:
        user.active_role = ActiveRole.CANDIDATE
    if payload.role in (UserRole.CANDIDATE, UserRole.BOTH) and not user.candidate_profile:
        db.add(CandidateProfile(user_id=user.id))
    if payload.role in (UserRole.REFERRER, UserRole.BOTH) and not user.referrer_profile:
        db.add(ReferrerProfile(user_id=user.id))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/switch-role", response_model=UserOut)
def switch_active_role(
    payload: ActiveRoleSwitch, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user.role == UserRole.CANDIDATE and payload.active_role == ActiveRole.REFERRER:
        raise HTTPException(status_code=400, detail="Become a referrer first")
    user.active_role = payload.active_role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/become-referrer", response_model=UserOut)
def become_referrer(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.referrer_profile:
        db.add(ReferrerProfile(user_id=user.id))
    if user.role == UserRole.CANDIDATE:
        user.role = UserRole.BOTH
    elif user.role != UserRole.BOTH:
        user.role = UserRole.REFERRER
    user.active_role = ActiveRole.REFERRER
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.get("/candidate", response_model=CandidateProfileOut)
def get_candidate_profile(user: User = Depends(get_current_user)):
    if not user.candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    return user.candidate_profile


@profile_router.put("/candidate", response_model=CandidateProfileOut)
def update_candidate_profile(
    payload: CandidateProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.candidate_profile:
        user.candidate_profile = CandidateProfile(user_id=user.id)
        db.add(user.candidate_profile)
    profile = user.candidate_profile
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@profile_router.post("/candidate/analyze", response_model=CandidateProfileOut)
def analyze_candidate_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.candidate_profile:
        raise HTTPException(status_code=404, detail="Complete your profile first")
    analysis = analyze_profile(user.candidate_profile)
    profile = user.candidate_profile
    profile.ai_summary = analysis.ai_summary
    profile.referral_readiness_score = analysis.referral_readiness_score
    profile.resume_suggestions = analysis.resume_suggestions
    add_reputation(db, user, "profile_completed", "AI profile analysis completed")
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@profile_router.get("/referrer", response_model=ReferrerProfileOut)
def get_referrer_profile(user: User = Depends(get_current_user)):
    if not user.referrer_profile:
        raise HTTPException(status_code=404, detail="Referrer profile not found")
    return user.referrer_profile


@profile_router.put("/referrer", response_model=ReferrerProfileOut)
def update_referrer_profile(
    payload: ReferrerProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.referrer_profile:
        user.referrer_profile = ReferrerProfile(user_id=user.id)
        db.add(user.referrer_profile)
    profile = user.referrer_profile
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    if profile.company_email and profile.company:
        profile.employment_verified = True
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
