from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models import AppUserRegistration, OrganizationCreate
from app.services.auth_service import post_user_organization_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register(
    session: SessionDep,
    user_data: AppUserRegistration,
    organization_data: OrganizationCreate,
):
    organization, admin_user = post_user_organization_service(
        session, user_data, organization_data
    )
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
