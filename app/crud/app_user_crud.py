from uuid import UUID
from sqlmodel import Session
from app.models import AppUserRegistration, AppUser


def create_admin_app_user(
    session: Session, user_data: AppUserRegistration, organization_id: UUID
):
    app_user = AppUser(
        **user_data.model_dump(),
        user_type_id="3e1208bc-aa8d-42d7-b957-95895a2f60aa",
        organization_id=organization_id,
    )
    session.add(app_user)
    session.flush()
    session.refresh(app_user)
    return app_user
