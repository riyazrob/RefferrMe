from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.enums import (
    ActiveRole,
    AuthProvider,
    Availability,
    EndorsementStatus,
    NotificationType,
    ReferralListingStatus,
    ReferralRequestStatus,
    UserRole,
)


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str | None = None
    auth_provider: AuthProvider = AuthProvider.EMAIL


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RoleSelect(BaseModel):
    role: UserRole


class ActiveRoleSwitch(BaseModel):
    active_role: ActiveRole


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    auth_provider: AuthProvider
    role: UserRole
    active_role: ActiveRole
    availability: Availability
    reputation_score: float
    verified: bool

    model_config = {"from_attributes": True}


class CandidateProfileUpdate(BaseModel):
    resume_text: str | None = None
    linkedin_url: str | None = None
    skills: str | None = None
    experience: str | None = None
    education: str | None = None
    certifications: str | None = None
    portfolio_url: str | None = None
    github_url: str | None = None
    work_authorization: str | None = None
    preferred_locations: str | None = None


class CandidateProfileOut(CandidateProfileUpdate):
    id: int
    user_id: int
    ai_summary: str | None = None
    referral_readiness_score: float | None = None
    resume_suggestions: str | None = None

    model_config = {"from_attributes": True}


class ReferrerProfileUpdate(BaseModel):
    company: str | None = None
    company_email: str | None = None
    title: str | None = None


class ReferrerProfileOut(ReferrerProfileUpdate):
    id: int
    user_id: int
    employment_verified: bool

    model_config = {"from_attributes": True}


class EndorsementCreate(BaseModel):
    endorser_name: str
    endorser_title: str
    endorser_email: EmailStr | None = None
    message: str | None = None


class EndorsementOut(BaseModel):
    id: int
    endorser_name: str
    endorser_title: str
    message: str | None
    status: EndorsementStatus

    model_config = {"from_attributes": True}


class ReferralCreate(BaseModel):
    company: str
    job_title: str
    job_link: str | None = None
    job_id: str | None = None
    job_description: str
    referral_deadline: datetime | None = None
    slots: int = Field(default=1, ge=1)


class ReferralUpdate(BaseModel):
    company: str | None = None
    job_title: str | None = None
    job_link: str | None = None
    job_id: str | None = None
    job_description: str | None = None
    parsed_role: str | None = None
    parsed_experience: str | None = None
    required_skills: str | None = None
    preferred_skills: str | None = None
    education_required: str | None = None
    certifications_required: str | None = None
    visa_sponsorship: bool | None = None
    location: str | None = None
    remote_ok: bool | None = None
    referral_deadline: datetime | None = None
    slots: int | None = Field(default=None, ge=1)


class ReferralOut(BaseModel):
    id: int
    referrer_id: int
    company: str
    job_title: str
    job_link: str | None
    job_id: str | None
    job_description: str
    parsed_role: str | None
    parsed_experience: str | None
    required_skills: str | None
    preferred_skills: str | None
    education_required: str | None
    certifications_required: str | None
    visa_sponsorship: bool
    location: str | None
    remote_ok: bool
    referral_deadline: datetime | None
    slots: int
    slots_filled: int
    status: ReferralListingStatus

    model_config = {"from_attributes": True}


class ReferralSearch(BaseModel):
    company: str | None = None
    role: str | None = None
    technology: str | None = None
    location: str | None = None
    remote: bool | None = None
    visa_sponsorship: bool | None = None


class ReferralRequestCreate(BaseModel):
    resume_version: str | None = None
    portfolio_url: str | None = None
    cover_message: str | None = None


class ReferralRequestOut(BaseModel):
    id: int
    referral_id: int
    candidate_id: int
    resume_version: str | None
    portfolio_url: str | None
    cover_message: str | None
    match_score: float | None
    match_explanation: str | None
    strengths: str | None
    missing_skills: str | None
    ai_recommendation: str | None
    status: ReferralRequestStatus

    model_config = {"from_attributes": True}


class StatusUpdate(BaseModel):
    status: ReferralRequestStatus


class ReviewDecision(BaseModel):
    accept: bool
    note: str | None = None


class NotificationOut(BaseModel):
    id: int
    type: NotificationType
    title: str
    message: str
    read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AIProfileAnalysis(BaseModel):
    ai_summary: str
    referral_readiness_score: float
    resume_suggestions: str


class AIJobParse(BaseModel):
    parsed_role: str
    parsed_experience: str
    required_skills: str
    preferred_skills: str
    education_required: str
    certifications_required: str
    visa_sponsorship: bool
    location: str
    remote_ok: bool


class AIMatchEvaluation(BaseModel):
    match_score: float
    match_explanation: str
    strengths: str
    missing_skills: str
    ai_recommendation: str


class WaitlistCreate(BaseModel):
    name: str
    email: EmailStr
    role: str | None = "both"


class WaitlistOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    confirmed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class WaitlistOutWithConfirm(WaitlistOut):
    confirmation_url: str | None = None

    model_config = {"from_attributes": True}
