from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import CurrentUserDep, SessionDep, TokenDep
from app.crud.app_user_crud import read_app_user_by_username
from app.models import AppUserRegistration, OrganizationCreate
from app.schemas.auth_schema import RegisterRequest
from app.services.auth_service import login_service, logout_service, register_service
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token_schema import Token

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
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return login_service(session, form_data)


@auth_router.get("/logout")
def logout(session: SessionDep, token: TokenDep):
    session.flush()
    return logout_service(session, token)
