import logging
import base64
import json

from botocore.exceptions import ClientError
from boto3 import session

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    secrets_session = session.Session()
    client = secrets_session.client(service_name="secretsmanager", region_name=region_name)
    secret = ""
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the
            # current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e

        raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary,
        # one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])
    return secret


def update_secret(secret_name, region_name, updated_value):
    secrets_session = session.Session()
    client = secrets_session.client(service_name="secretsmanager", region_name=region_name)

    try:
        add_secret_value_response = client.update_secret(SecretId=secret_name, SecretString=json.dumps(updated_value))

        return add_secret_value_response
    except ClientError as e:
        logger.info("Update of Secret Response Failed")
        raise e