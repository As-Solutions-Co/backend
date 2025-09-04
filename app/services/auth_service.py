from sqlmodel import Session
from app.models import AppUserRegistration, OrganizationCreate
from app.services.document_type_service import get_document_type_by_id_service
from app.crud.organization_crud import create_organization
from app.crud.app_user_crud import create_admin_app_user


def post_user_organization_service(
    session: Session,
    user_data: AppUserRegistration,
    organization_data: OrganizationCreate,
):
    try:
        organization = create_organization(session, organization_data)
        admin_user = create_admin_app_user(session, user_data, organization.id)
        session.commit()
        session.refresh(organization)
        session.refresh(admin_user)
        return organization, admin_user
    except Exception:
        session.rollback()
        raise
