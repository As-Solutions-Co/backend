from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.document_type_crud import (
    read_document_type_by_id,
    read_document_types_by_country_id,
)
from app.models import DocumentType


def get_document_types_by_country_service(
    session: Session, country_id: UUID
) -> list[DocumentType] | None:
    document_types = read_document_types_by_country_id(session, country_id)
    if not document_types:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Document types not found with this country id"
        )
    return document_types


def get_document_type_by_id_service(
    session: Session, id: UUID
) -> list[DocumentType] | None:
    document_types = read_document_type_by_id(session, id)
    if not document_types:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Document type not found with this id"
        )
    return document_types
