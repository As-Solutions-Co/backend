from .mixins import IdMixin
from sqlmodel import Field
from sqlalchemy import func
from datetime import datetime


class InvalidToken(IdMixin, table=True):
    token: str
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
