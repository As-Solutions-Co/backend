import json
import os

import boto3
from botocore.exceptions import ClientError
from sqlmodel import create_engine

secret_id = os.getenv("SECRET_ARN")
region_name = "us-east-1"
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=region_name)

try:
    get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    secret = json.loads(get_secret_value_response["SecretString"])
    USERNAME = secret["username"]
    PASSWORD = secret["password"]
    HOST = secret["host"]
    PORT = secret["port"]
    DB_NAME = os.getenv("DB_NAME")
    DB_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    engine = create_engine(DB_URL)

except (ClientError, KeyError, ValueError) as e:
    raise e
