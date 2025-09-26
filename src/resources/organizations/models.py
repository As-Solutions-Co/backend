from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class OrganizationBase(SQLModel):
    name: str
    main_color: str
    logo: str


class Organization(OrganizationBase, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)


class OrganizationCreate(OrganizationBase): ...


class OrganizationPublic(OrganizationBase): ...
