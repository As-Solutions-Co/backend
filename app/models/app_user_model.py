from uuid import UUID

from sqlmodel import Field, SQLModel, UniqueConstraint

from app.models.mixins import MixinBase


class AppUserBase(SQLModel):
    username: str
    password: str


class AppUserCreate(AppUserBase): ...


class AppUser(AppUserBase, MixinBase, table=True):
    is_active: bool = Field(default=True)
    organization_id: UUID = Field(foreign_key="organization.id")
    __tablename__ = "app_user"
