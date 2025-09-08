from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models.country_model import CountriesPublic, Country
from app.services.country_service import get_countries_service, get_country_service

country_router = APIRouter(prefix="/countries", tags=["Countries"])


@country_router.get("/", response_model=CountriesPublic)
def get_countries(
    session: SessionDep, skip: int = 0, limit: int = 10, name: str = None
):
    return get_countries_service(session, skip, limit, name)


@country_router.get("/{country_id}", response_model=Country)
def get_country(session: SessionDep, country_id: UUID):
    return get_country_service(session, country_id)
