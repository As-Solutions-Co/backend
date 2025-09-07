from uuid import UUID
from sqlmodel import SQLModel, Field, UniqueConstraint

from app.models.mixins import MixinBase


class OrganizationBase(SQLModel):
    name: str
    logo: str
    main_color: str


class Organization(MixinBase, OrganizationBase, table=True):
    pass


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: UUID
