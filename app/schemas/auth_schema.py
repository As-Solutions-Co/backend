from pydantic import BaseModel

from app.models.app_user_model import AppUserCreate
from app.models.organization_model import OrganizationCreate


class RegisterRequest(BaseModel):
    user_data: AppUserCreate
    organization_data: OrganizationCreate
