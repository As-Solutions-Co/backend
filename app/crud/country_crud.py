from sqlmodel import select, Session
from app.models.country import Country
from typing import List, Optional
from uuid import UUID


def get_all_countries(
    session: Session, skip: int = 0, limit: int = 10
) -> List[Country]:
    stmt = select(Country).offset(skip).limit(limit)
    return session.exec(stmt).all()


def get_country_by_id(session: Session, country_id: UUID) -> Optional[Country]:
    stmt = select(Country).where(Country.id == country_id)
    return session.exec(stmt).first()
