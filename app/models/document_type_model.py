from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, select

from app.models import Country
from app.models.mixins import MixinBase


class DocumentTypeBase(MixinBase):
    name: str = Field(max_length=20)
    abreviation: str = Field(max_length=8)


class DocumentType(DocumentTypeBase, table=True):
    __tablename__ = "document_type"
    country_id: UUID = Field(foreign_key="country.id")


class DocumentTypeResponse(DocumentTypeBase):
    pass
