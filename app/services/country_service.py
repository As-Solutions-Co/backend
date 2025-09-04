from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.country_crud import (
    get_all_countries,
    get_country_by_id,
    get_country_by_name,
)
from app.models.country_model import CountriesPublic, Country


def get_countries_service(
    session: Session, skip: int = 0, limit: int = 10, name: str = None
) -> CountriesPublic:
    if name:
        countries = get_country_by_name(session, name)
        if not countries:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Countries not found")
    else:
        countries = get_all_countries(session, skip, limit)
    total = len(get_all_countries(session, 0, None))
    return CountriesPublic(data=countries, count=total)


def get_country_service(session: Session, country_id: UUID) -> Country:
    country = get_country_by_id(session, country_id)
    if not country:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Country not found")
    return country
