from uuid import UUID
from app.models.mixins import MixinBase
from sqlmodel import SQLModel, Field


class UserTypeBase(SQLModel):
    name: str = Field(max_length=10)


class UserType(MixinBase, UserTypeBase, table=True):
    __tablename__ = "user_type"


class UserTypeResponse(UserTypeBase):
    id: UUID
