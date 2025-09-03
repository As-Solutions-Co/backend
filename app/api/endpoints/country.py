from uuid import UUID
from fastapi import APIRouter, Query
from app.models import CountriesPublic, Country
from app.api.deps import SessionDep
from app.services.country_service import get_countries_service, get_country_service

country_router = APIRouter(prefix="/countries", tags=["Countries"])


@country_router.get("/", response_model=CountriesPublic)
def get_countries(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Máximo de elementos a retornar"),
):
    return get_countries_service(session, skip=skip, limit=limit)


@country_router.get("/{country_id}", response_model=Country)
def get_country(session: SessionDep, country_id: UUID):
    return get_country_service(session, country_id)
