from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, select
from app.models import Country


class DocumentType(SQLModel, table=True):
    __tablename__ = "document_type"
    id: UUID = Field(primary_key=True)
    name: str = Field(max_length=20)
    abreviation: str = Field(max_length=8)
    country: UUID = Field(foreign_key="country.id")
