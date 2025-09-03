from fastapi import APIRouter

from app.api.endpoints import country_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(country_router)
