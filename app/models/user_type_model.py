from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.mixins import MixinBase


class UserTypeBase(SQLModel):
    name: str = Field(max_length=10)


class UserType(MixinBase, UserTypeBase, table=True):
    __tablename__ = "user_type"


class UserTypeResponse(UserTypeBase):
    id: UUID
