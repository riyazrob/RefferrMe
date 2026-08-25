from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import EndorsementStatus


class Endorsement(Base):
    __tablename__ = "endorsements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_profile_id: Mapped[int] = mapped_column(ForeignKey("candidate_profiles.id"))
    endorser_name: Mapped[str] = mapped_column(String(255))
    endorser_title: Mapped[str] = mapped_column(String(255))
    endorser_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[EndorsementStatus] = mapped_column(Enum(EndorsementStatus), default=EndorsementStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate_profile: Mapped["CandidateProfile"] = relationship(back_populates="endorsements")
