from uuid import UUID
from sqlmodel import Session
from app.models import AppUserRegistration, AppUser


def create_app_user(session: Session, user_data: AppUser):
    app_user = AppUser(**user_data.model_dump())
    session.add(app_user)
    session.flush()
    session.refresh(app_user)
    return app_user
