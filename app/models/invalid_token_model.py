from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field

from .mixins import IdMixin


class InvalidToken(IdMixin, table=True):
    token: str
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )

    __tablename__ = "invalid_token"
