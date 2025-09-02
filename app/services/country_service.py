from app.crud.country_crud import get_all_countries, get_country_by_id
from app.models.country import CountriesPublic, Country
from sqlmodel import Session
from uuid import UUID


def get_countries_service(
    session: Session, skip: int = 0, limit: int = 10
) -> CountriesPublic:
    from sqlmodel import select

    total = len(session.exec(select(Country)).all())
    countries = get_all_countries(session, skip=skip, limit=limit)
    return CountriesPublic(data=countries, count=total)


def get_country_service(session: Session, country_id: UUID) -> Country:
    country = get_country_by_id(session, country_id)
    if not country:
        from fastapi import HTTPException, status

        raise HTTPException(status.HTTP_404_NOT_FOUND, "Country not found")
    return country
