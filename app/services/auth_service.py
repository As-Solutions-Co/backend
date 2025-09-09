from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.security import generate_token, verify_password
from app.crud.app_user_crud import create_app_user, read_app_user_by_username
from app.crud.invalid_token_crud import create_invalid_token
from app.crud.organization_crud import (
    read_organization_by_dane_code,
    read_organization_by_id,
)
from app.models import Organization
from app.models.app_user_model import AppUser
from app.models.invalid_token_model import InvalidToken
from app.schemas.auth_schema import RegisterRequest
from app.schemas.token_schema import Token
from app.utils.dane import get_legal_information_from_dane


def register_service(session: Session, register_data: RegisterRequest):
    organization_in = register_data.organization_data
    try:
        if read_organization_by_dane_code(session, organization_in.dane_code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An organization with this dane_code already exists.",
            )

        organization_dane = get_legal_information_from_dane(organization_in.dane_code)
        if not organization_dane:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization with dane_code {organization_in.dane_code} not found.",
            )

        organization_data = organization_in.model_dump()
        organization_data.update(organization_dane.model_dump())
        organization = Organization(**organization_data)
        session.add(organization)
        session.flush()
        user_in = register_data.user_data
        user = create_app_user(
            session, AppUser(**user_in.model_dump(), organization_id=organization.id)
        )
        session.commit()
        session.refresh(organization)
        session.refresh(user)
        return organization, user
    except IntegrityError:
        session.rollback()


def login_service(session: Session, form_data: OAuth2PasswordRequestForm) -> Token:
    username = form_data.username
    password = form_data.password
    user = read_app_user_by_username(session, username)

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    organization = read_organization_by_id(session, user.organization_id)
    payload = {
        "user_id": str(user.id),
        "organization_id": str(organization.id),
        "main_color": str(organization.main_color),
    }
    token = generate_token(payload)
    return Token(access_token=token)


def logout_service(session: Session, token: str) -> InvalidToken:
    try:
        invalid_token = create_invalid_token(session, token)
        session.commit()
        return invalid_token
    except Exception as e:
        print(e)
        session.rollback()
