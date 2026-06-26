import boto3
import os
import pytest

from moto import mock_s3, mock_dynamodb, mock_lambda

os.environ["region"] = "us-east-1"
os.environ["Role"] = "arn:aws:iam::123456789:role/does-not-exist"
os.environ["secretName"] = "prod/groupmanager"


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)
    
@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["x-api-key"] = "da2-test"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
