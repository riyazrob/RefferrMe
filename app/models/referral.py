from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import ReferralListingStatus, ReferralRequestStatus


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(255))
    job_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    job_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    job_description: Mapped[str] = mapped_column(Text)
    parsed_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parsed_experience: Mapped[str | None] = mapped_column(String(255), nullable=True)
    required_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    education_required: Mapped[str | None] = mapped_column(Text, nullable=True)
    certifications_required: Mapped[str | None] = mapped_column(Text, nullable=True)
    visa_sponsorship: Mapped[bool] = mapped_column(default=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_ok: Mapped[bool] = mapped_column(default=False)
    referral_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    slots: Mapped[int] = mapped_column(Integer, default=1)
    slots_filled: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[ReferralListingStatus] = mapped_column(
        Enum(ReferralListingStatus), default=ReferralListingStatus.DRAFT
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    referrer: Mapped["User"] = relationship(back_populates="referrals_posted")
    requests: Mapped[list["ReferralRequest"]] = relationship(back_populates="referral")


class ReferralRequest(Base):
    __tablename__ = "referral_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referral_id: Mapped[int] = mapped_column(ForeignKey("referrals.id"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    resume_version: Mapped[str | None] = mapped_column(Text, nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    match_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    match_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    missing_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReferralRequestStatus] = mapped_column(
        Enum(ReferralRequestStatus), default=ReferralRequestStatus.REQUESTED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    referral: Mapped["Referral"] = relationship(back_populates="requests")
    candidate: Mapped["User"] = relationship(back_populates="referral_requests")
