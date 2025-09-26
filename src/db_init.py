from db import engine
from organizations.models import Organization as Organization
from sqlmodel import SQLModel
from students.models import Student as Student


def handler(event, context):  # noqa
    try:
        SQLModel.metadata.create_all(engine)
        return {"message": "success"}
    except Exception as e:
        return e.__str__()
