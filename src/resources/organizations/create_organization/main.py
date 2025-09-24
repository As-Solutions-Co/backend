import boto3
from botocore.exceptions import ClientError
import json
from sqlalchemy import create_engine, text
import os


def get_secret():
    secret_name = os.getenv("SECRET_NAME")
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]

    username = secret["username"]
    password = secret["password"]

    return username, password


def get_session():
    username, password = get_secret()
    host = "academy.c89aw02c2ls0.us-east-1.rds.amazonaws.com"
    port = 5432

    db_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/postgres"

    return create_engine(db_url)


def handler(event, context):
    engine = get_session()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1;"))

    return json.dumps(
        {
            "status_code": 200,
            "message": "hi",
        }
    )
