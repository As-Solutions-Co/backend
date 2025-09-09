from uuid import UUID

from sqlmodel import Session, select

from app.models.organization_model import Organization


def create_organization(session: Session, organization: Organization) -> Organization:
    session.add(organization)
    return organization


def read_organization_by_name(session: Session, name: str) -> Organization | None:
    stmt = select(Organization).where(Organization.name == name)
    return session.exec(stmt).first()


def read_organization_by_id(session: Session, id: UUID) -> Organization | None:
    stmt = select(Organization).where(Organization.id == id)
    return session.exec(stmt).first()


def read_organization_by_dane_code(session: Session, code: str) -> Organization | None:
    stmt = select(Organization).where(Organization.dane_code == code)
    return session.exec(stmt).first()
