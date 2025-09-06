from fastapi import APIRouter

from app.api.endpoints import auth_router, country_router, document_type_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(country_router)
api_router.include_router(document_type_router)
api_router.include_router(auth_router)
