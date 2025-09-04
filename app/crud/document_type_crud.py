from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import DocumentType


def read_document_types(
    session: Session, skip: int = 0, limit: int | None = 10
) -> List[DocumentType]:
    stmt = select(DocumentType)
    return session.exec(stmt).all()


def read_document_type_by_id(session: Session, id: UUID) -> DocumentType | None:
    stmt = select(DocumentType).where(DocumentType.id == id)
    return session.exec(stmt).first()


def read_document_types_by_country_id(
    session: Session, country_id: UUID
) -> List[DocumentType] | None:
    stmt = select(DocumentType).where(DocumentType.country == country_id)
    return session.exec(stmt).all()


def read_document_type_by_name(
    session: Session, name: str
) -> List[DocumentType] | None:
    stmt = select(DocumentType).where(DocumentType.name.ilike(f"{name}%"))
    return session.exec(stmt).all()
