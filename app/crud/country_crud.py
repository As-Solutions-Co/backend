from uuid import UUID

from sqlmodel import Session, select

from app.models.country_model import Country


def get_all_countries(
    session: Session, skip: int = 0, limit: int | None = 10
) -> list[Country]:
    stmt = select(Country).offset(skip).limit(limit)
    return session.exec(stmt).all()


def get_country_by_id(session: Session, country_id: UUID) -> Country | None:
    stmt = select(Country).where(Country.id == country_id)
    return session.exec(stmt).first()


def get_country_by_name(session: Session, name: str) -> Country | None:
    stmt = select(Country).where(Country.nice_name.ilike(f"{name}%"))
    return session.exec(stmt).all()
