from uuid import UUID

from db import engine
from models import Organization
from sqlmodel import Session, select


def read_organization():
    with Session(engine) as session:
        stmt = select(Organization)
        return session.exec(stmt).all()


def read_organization_by_id(id: UUID):
    with Session(engine) as session:
        stmt = select(Organization).where(Organization.id == id)
        return session.exec(stmt).first()
