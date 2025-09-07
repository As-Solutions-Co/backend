from sqlmodel import Session
from app.models import Organization, OrganizationCreate


def create_organization(
    session: Session, organization_data: OrganizationCreate
) -> Organization:
    organization = Organization(**organization_data.model_dump())
    session.add(organization)
    session.flush()
    session.refresh(organization)
    return organization
