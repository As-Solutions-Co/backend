from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..models import CountriesPublic, Country
from app.api.deps import SessionDep

country_router = APIRouter(prefix="/countries", tags=["Countries"])


@country_router.get("/", response_model=CountriesPublic)
def get_countries(session: SessionDep):
    stmt = select(Country)
    countries = session.exec(stmt).all()
    return CountriesPublic(data=countries, count=len(countries))


@country_router.get("/{country_id}", response_model=Country)
def get_country(session: SessionDep, country_id: UUID):
    stmt = select(Country).where(Country.id == country_id)
    country = session.exec(stmt).first()
    if not country:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Country not found")
    return country
