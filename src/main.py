import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "rds!db-dca1ac4a-ca72-4ba3-8e38-fd233986ad88"
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

    return get_secret_value_response["SecretString"]

    # Your code goes here.


print(get_secret())
