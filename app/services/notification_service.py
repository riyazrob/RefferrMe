from sqlalchemy.orm import Session

from app.enums import NotificationType
from app.models.notification import Notification
from app.models.user import User


def create_notification(
    db: Session,
    user: User,
    type: NotificationType,
    title: str,
    message: str,
) -> Notification:
    notification = Notification(user_id=user.id, type=type, title=title, message=message)
    db.add(notification)
    return notification


def mark_read(db: Session, notification: Notification) -> None:
    notification.read = True
    db.add(notification)
