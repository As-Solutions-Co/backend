from uuid import UUID

from sqlmodel import Session, select

from app.models import AppUser


def create_app_user(session: Session, user_data: AppUser):
    app_user = AppUser(**user_data.model_dump())
    session.add(app_user)
    session.flush()
    session.refresh(app_user)
    return app_user


def read_app_user_by_username(session: Session, username: str) -> AppUser | None:
    stmt = select(AppUser).where(AppUser.username == username)
    return session.exec(stmt).first()


def read_app_user_by_id(session: Session, id: UUID) -> AppUser | None:
    stmt = select(AppUser).where(AppUser.id == id)
    return session.exec(stmt).first()
