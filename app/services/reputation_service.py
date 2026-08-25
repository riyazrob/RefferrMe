from sqlalchemy.orm import Session

from app.models.reputation import ReputationEvent
from app.models.user import User

POINTS = {
    "profile_completed": 10,
    "endorsement_received": 5,
    "referral_accepted": 15,
    "referral_submitted": 10,
    "referral_joined": 50,
    "referral_declined": -2,
    "successful_hire_referrer": 30,
    "fast_response": 5,
}


def add_reputation(db: Session, user: User, event_type: str, description: str | None = None) -> None:
    points = POINTS.get(event_type, 0)
    if points == 0:
        return
    event = ReputationEvent(user_id=user.id, event_type=event_type, points=points, description=description)
    user.reputation_score = round(user.reputation_score + points, 1)
    db.add(event)
    db.add(user)
