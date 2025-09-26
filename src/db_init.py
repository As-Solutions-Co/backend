from sqlmodel import SQLModel
from db import engine
from organizations.models import Organization  # noqa


def handler(event, context):
    try:
        SQLModel.metadata.create_all(engine)
        return {"message": "success"}
    except Exception as e:
        return e.__str__()
