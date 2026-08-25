from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.notification import Notification
from app.models.user import User
from app.schemas import NotificationOut, UserCreate, UserLogin, UserOut
from app.services.auth_service import hash_password, verify_password
from app.models.profile import CandidateProfile

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=UserOut, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=payload.email,
        name=payload.name,
        auth_provider=payload.auth_provider,
        password_hash=hash_password(payload.password) if payload.password else None,
    )
    db.add(user)
    db.flush()
    db.add(CandidateProfile(user_id=user.id))
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


notifications_router = APIRouter(prefix="/notifications", tags=["notifications"])


@notifications_router.get("", response_model=list[NotificationOut])
def list_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()


@notifications_router.post("/{notification_id}/read", response_model=NotificationOut)
def read_notification(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from fastapi import HTTPException
    from app.services.notification_service import mark_read
    notification = db.get(Notification, notification_id)
    if not notification or notification.user_id != user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    mark_read(db, notification)
    db.commit()
    db.refresh(notification)
    return notification
