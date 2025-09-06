from sqlmodel import Field, SQLModel
from sqlalchemy import func
from uuid import UUID, uuid4
from datetime import datetime


class IdMixin(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4)


class MixinBase(IdMixin):
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
        nullable=False,
    )
