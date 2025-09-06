from pydantic import BaseModel

from app.models import AppUserRegistration, OrganizationCreate


class RegisterRequest(BaseModel):
    user_data: AppUserRegistration
    organization_data: OrganizationCreate
