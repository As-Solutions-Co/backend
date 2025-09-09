from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.mixins import MixinBase


class OrganizationBase(SQLModel):
    main_color: str


class OrganizationDane(SQLModel):
    dane_code: str = Field(unique=True)
    logo: str = Field(nullable=True, default=None)
    name: str
    address: str
    latitude: float
    longitude: float


class Organization(MixinBase, OrganizationDane, OrganizationBase, table=True): ...


class OrganizationCreate(OrganizationBase):
    dane_code: str


class OrganizationResponse(OrganizationBase):
    id: UUID
