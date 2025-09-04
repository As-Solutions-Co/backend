from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, select

from app.models import Country


class DocumentTypeBase(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str = Field(max_length=20)
    abreviation: str = Field(max_length=8)


class DocumentType(DocumentTypeBase, table=True):
    __tablename__ = "document_type"
    country: UUID = Field(foreign_key="country.id")


class DocumentTypeResponse(DocumentTypeBase):
    pass
