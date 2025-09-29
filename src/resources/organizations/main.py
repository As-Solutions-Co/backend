from uuid import UUID

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    NotFoundError,
)
from crud import read_organization, read_organization_by_id
from db import engine
from models import Organization, OrganizationCreate
from sqlmodel import Session

app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/organizations/swagger",
    title="Organizations microservice documentation",
)


@app.get("/organizations")
def get_organizations() -> list[Organization]:
    result = read_organization()
    return result


@app.get("/organizations/<id>")
def get_organization(id: UUID) -> Organization:
    result = read_organization_by_id(id)
    if not result:
        raise NotFoundError("Organization not found")
    return result


@app.post("/organizations")
def post_organization(payload: OrganizationCreate) -> Organization:
    with Session(engine) as session:
        try:
            organization_in = Organization(**payload.model_dump())
            session.add(organization_in)
            session.commit()
            session.refresh(organization_in)
            return organization_in, 201
        except Exception as e:
            raise InternalServerError(f"Error creating organization, {e.__str__()}")


@app.delete("/organizations/<id>")
def delete_organization(id: UUID) -> Organization:
    result = read_organization_by_id(id)
    if not result:
        raise NotFoundError("Organization not found")
    try:
        with Session(engine) as session:
            session.delete(result)
            session.commit()
        return "", 204
    except Exception as e:
        raise InternalServerError(f"Error deleting organization, {e.__str__()}")


def handler(event, context):
    return app.resolve(event, context)


## Validate options method
