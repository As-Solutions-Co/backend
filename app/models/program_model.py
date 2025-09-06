from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.mixins import MixinBase


class ProgramBase(SQLModel):
    name: str


class Program(MixinBase, ProgramBase, table=True):
    organization_id: UUID = Field(foreign_key="organization.id")


class ProgramResponse(ProgramBase):
    id: UUID
