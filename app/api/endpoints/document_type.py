from typing import List
from uuid import UUID
from fastapi import APIRouter
from sqlmodel import join, select

from app.api.deps import SessionDep
from app.models import DocumentType
from app.models.country_model import Country
from app.models.document_type_model import DocumentTypeResponse
from app.services.document_type_service import get_document_types_by_country_service

document_type_router = APIRouter(prefix="/document_type", tags=["Document type"])


@document_type_router.get("/{country_id}", response_model=List[DocumentTypeResponse])
def get_document_types_with_country(session: SessionDep, country_id: UUID):
    return get_document_types_by_country_service(session, country_id)
