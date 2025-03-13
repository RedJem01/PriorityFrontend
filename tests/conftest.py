import os

import boto3
import pytest
from moto import mock_aws

REGION='eu-west-2'

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def sqs_client(aws_credentials):
    # setup
    with mock_aws():
        yield boto3.client('sqs', region_name=REGION)

@pytest.fixture(scope='function')
def bedrock_client(aws_credentials):
    # setup
    with mock_aws():
        yield boto3.client('bedrock', region_name=REGION)