from .auth import auth_router
from .country import country_router
from .document_type import document_type_router

__all__ = ["country_router", "document_type_router", "auth_router"]
