from datetime import date, datetime
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Column, Field, SQLModel, UniqueConstraint
from sqlalchemy import Enum as SqlEnum

from app.models.mixins import MixinBase


from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class AppUserBase(SQLModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    document_type_id: UUID = Field(foreign_key="document_type.id")
    document_number: str = Field(max_length=40)
    username: str = Field(max_length=12)
    email: EmailStr
    phone: str
    birthdate: date
    institutional_email: EmailStr
    status: str = Field(
        sa_column=Column(SqlEnum(UserStatus, name="userstatus")),
        default=UserStatus.ACTIVE,
    )
    address: str


class AppUser(MixinBase, AppUserBase, table=True):
    __tablename__ = "app_user"
    __table_args__ = (UniqueConstraint("document_number", "organization_id"),)

    organization_id: UUID = Field(foreign_key="organization.id")
    password: str
    user_type_id: UUID = Field(foreign_key="user_type.id")


class AppUserRegistration(AppUserBase):
    password: str


class AppUserResponse(AppUserBase):
    id: UUID
    organization_id: UUID
