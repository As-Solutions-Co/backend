from uuid import UUID

from sqlmodel import Session, select

from app.models.user_type_model import UserType


def read_all_user_types(session: Session) -> list[UserType]:
    stmt = select(UserType)
    return session.exec(stmt).all()


def read_user_type_by_id(session: Session, user_type_id: UUID) -> UserType | None:
    stmt = select(UserType).where(UserType.id == user_type_id)
    return session.exec(stmt).first()


def read_user_type_by_name(session: Session, name: str) -> UserType | None:
    stmt = select(UserType).where(UserType.name == name)
    return session.exec(stmt).first()
