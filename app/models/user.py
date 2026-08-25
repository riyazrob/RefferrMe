from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import ActiveRole, AuthProvider, Availability, UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    auth_provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider), default=AuthProvider.EMAIL)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CANDIDATE)
    active_role: Mapped[ActiveRole] = mapped_column(Enum(ActiveRole), default=ActiveRole.CANDIDATE)
    availability: Mapped[Availability] = mapped_column(Enum(Availability), default=Availability.LOOKING)
    reputation_score: Mapped[float] = mapped_column(Float, default=0.0)
    verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate_profile: Mapped["CandidateProfile | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    referrer_profile: Mapped["ReferrerProfile | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    referrals_posted: Mapped[list["Referral"]] = relationship(back_populates="referrer")
    referral_requests: Mapped[list["ReferralRequest"]] = relationship(back_populates="candidate")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    reputation_events: Mapped[list["ReputationEvent"]] = relationship(back_populates="user")
