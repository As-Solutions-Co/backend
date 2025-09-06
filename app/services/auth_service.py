from uuid import UUID
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.crud.document_type_crud import read_document_type_by_id
from app.crud.user_type import read_user_type_by_name
from app.crud.organization_crud import create_organization, read_organization_by_name
from app.crud.app_user_crud import create_app_user
from app.models.app_user_model import AppUser
from app.models import Organization, AppUser as AppUserModel
from app.schemas.auth_schema import RegisterRequest
from app.utils.security import hash_password


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
