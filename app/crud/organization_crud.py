from sqlmodel import Session, select
from app.models import Organization, OrganizationCreate


def create_organization(
    session: Session, organization_data: OrganizationCreate
) -> Organization:
    organization = Organization(**organization_data.model_dump())
    session.add(organization)
    session.flush()
    session.refresh(organization)
    return organization


def read_organization_by_name(session: Session, name: str) -> Organization | None:
    stmt = select(Organization).where(Organization.name == name)
    return session.exec(stmt).first()
