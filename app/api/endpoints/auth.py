from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models import AppUserRegistration, OrganizationCreate
from app.schemas.auth_schema import RegisterRequest
from app.services.auth_service import register_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register(session: SessionDep, register_data: RegisterRequest):
    organization, admin_user = register_service(session, register_data)
    return {
        "organization": organization,
        "admin_user": admin_user,
    }


@auth_router.post("/login")
def login(
    session: SessionDep,
    organization_data: OrganizationCreate,
): ...


@auth_router.get("/logout")
def logout():
    pass
