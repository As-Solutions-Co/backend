import json
from sqlmodel import select, Session
from models import Organization
from db import engine
from uuid import UUID


def read_organization():
    with Session(engine) as session:
        stmt = select(Organization)
        return session.exec(stmt).all()
