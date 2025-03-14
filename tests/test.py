import json
from unittest.mock import patch

from moto import mock_aws

import main
from main import app

aws_region = "eu-west-2"

def set_environment_variables():
    main.P1_QUEUE = ''
    main.P2_QUEUE = ''
    main.P3_QUEUE = ''
    main.AWS_REGION = aws_region
    main.ACCESS_KEY = 'testing'
    main.SECRET_ACCESS_KEY = 'testing'

@patch('main.bedrock_suggestion')
def test_priority_form_queue_1(bedrock_suggestion_mock, sqs_client):
    set_environment_variables()
    queue1 = sqs_client.create_queue(QueueName='queue1')

    queue_url1 = queue1['QueueUrl']

    # override function global URL variable
    main.P1_QUEUE = queue_url1

    bedrock_suggestion_mock.return_value = "Bedrock response"

    client = app.test_client()
    client.post("/", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "High"
    })

    expected_msg = {'description': 'Happening right now\n\n Suggested fix: \n\nBedrock response','title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url1)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

@patch('main.bedrock_suggestion')
def test_priority_form_queue_2(bedrock_suggestion_mock, sqs_client):
    set_environment_variables()
    queue2 = sqs_client.create_queue(QueueName='queue2')

    queue_url2 = queue2['QueueUrl']

    # override function global URL variable
    main.P2_QUEUE = queue_url2

    bedrock_suggestion_mock.return_value = "Bedrock response"

    client = app.test_client()
    client.post("/", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "Medium"
    })

    expected_msg = {'description': 'Happening right now\n\n Suggested fix: \n\nBedrock response','title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url2)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

@patch('main.bedrock_suggestion')
def test_priority_form_queue_3(bedrock_suggestion_mock, sqs_client):
    set_environment_variables()
    queue3 = sqs_client.create_queue(QueueName='queue3')

    queue_url3 = queue3['QueueUrl']

    # override function global URL variable
    main.P3_QUEUE = queue_url3

    bedrock_suggestion_mock.return_value = "Bedrock response"

    client = app.test_client()
    client.post("/", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "Low"
    })

    expected_msg = {'description': 'Happening right now\n\n Suggested fix: \n\nBedrock response','title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url3)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200