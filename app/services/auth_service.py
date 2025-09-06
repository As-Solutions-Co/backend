from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.crud.app_user_crud import create_app_user, read_app_user_by_username
from app.crud.document_type_crud import read_document_type_by_id
from app.crud.invalid_token_crud import create_invalid_token
from app.crud.organization_crud import (
    create_organization,
    read_organization_by_id,
    read_organization_by_name,
)
from app.crud.user_type import read_user_type_by_name
from app.models import AppUser as AppUserModel
from app.models import Organization
from app.models.app_user_model import AppUser
from app.models.invalid_token_model import InvalidToken
from app.schemas.auth_schema import RegisterRequest
from app.schemas.token_schema import Token
from app.utils.security import check_password, generate_token, hash_password


def register_service(
    session: Session, register_data: RegisterRequest
) -> dict[str, Organization | AppUserModel]:
    organization_data = register_data.organization_data
    user_data = register_data.user_data

    if read_organization_by_name(session, organization_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An organization with this name already exists.",
        )

    document_type = read_document_type_by_id(session, user_data.document_type_id)
    if not document_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document type with id {user_data.document_type_id} not found",
        )

    admin_user_type = read_user_type_by_name(session, name="admin")

    try:
        new_organization = create_organization(session, organization_data)
        session.flush()

        user_data_extended = AppUser(
            **user_data.model_dump(),
            organization_id=new_organization.id,
            user_type_id=admin_user_type.id,
        )

        user_data_extended.password = hash_password(user_data_extended.password)

        admin_user = create_app_user(session, user_data_extended)

        session.commit()
        session.refresh(new_organization)
        session.refresh(admin_user)

        return {"organization": new_organization, "admin_user": admin_user}

    except SQLAlchemyError:
        session.rollback()
        raise


def login_service(session: Session, form_data: OAuth2PasswordRequestForm) -> Token:
    username = form_data.username
    password = form_data.password
    user = read_app_user_by_username(session, username)

    if not user or not check_password(password, user.password):
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
    except:
        session.rollback()
