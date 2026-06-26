from moto import mock_dynamodb, mock_lambda
from moto import settings, mock_iam
import zipfile
import io
from botocore.exceptions import ClientError
import boto3

def get_role_name():
    with mock_iam():
        iam = boto3.client("iam", region_name="us-east-1")
        try:
            return iam.get_role(RoleName="my-role")["Role"]["Arn"]
        except ClientError:
            return iam.create_role(
                RoleName="my-role",
                AssumeRolePolicyDocument="some policy",
                Path="/my-path/",
            )["Role"]["Arn"]
            
# Expected response setup and zip file for lambda mock creation
def lambda_getAvailableRooms():
    code = '''
import json
def lambda_handler(event, context):
    return {
        "body": {
            "rooms": ["r1", "r2", "r3"],
            "totalRoom": 3
        }
    }
            '''
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr('lambda_function.py', code)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read() 

def lambda_getAvailableJudges():
    code = '''
import json
def lambda_handler(event, context):
    return {
        "body": {
            "judges": ["j1", "j2", "j3", "j4", "j5", "j6", "j7"],
            "totalJudge": 7
        }
    }
            '''
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr('lambda_function.py', code)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read() 

def lambda_normal():
    code = '''
import json
def lambda_handler(event, context):
    return event
            '''
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr('lambda_function.py', code)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read() 

# create mocked lambda with zip file
def mock_some_lambda(client, lambda_name, return_event):
    return client.create_function(
        FunctionName=lambda_name,
        Runtime='python3.7',
        Role=get_role_name(),
        Handler='lambda_function.lambda_handler',
        Code={
            'ZipFile': return_event,
        },
        Publish=True,
        Timeout=30,
        MemorySize=128
    )