from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from crud import read_organization

app = APIGatewayRestResolver()


@app.get("/organization")
def get_organization():
    result = read_organization()
    return {"data": result}


def handler(event, context):
    return app.resolve(event, context)
