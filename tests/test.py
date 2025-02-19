import json

import main
from main import app

def set_environment_variables():
    main.P1_QUEUE = ''
    main.P2_QUEUE = ''
    main.P3_QUEUE = ''
    main.AWS_REGION = 'eu-west-2'
    main.ACCESS_KEY = 'testing'
    main.SECRET_ACCESS_KEY = 'testing'

def test_priority_form_queue_1(sqs_client):
    set_environment_variables()
    queue1 = sqs_client.create_queue(QueueName='queue1')

    queue_url1 = queue1['QueueUrl']

    # override function global URL variable
    main.P1_QUEUE = queue_url1

    client = app.test_client()
    client.post("/form", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "High"
    })

    expected_msg = {'description': 'Happening right now', 'title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url1)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

def test_priority_form_queue_2(sqs_client):
    set_environment_variables()
    queue2 = sqs_client.create_queue(QueueName='queue2')

    queue_url2 = queue2['QueueUrl']

    # override function global URL variable
    main.P2_QUEUE = queue_url2

    client = app.test_client()
    client.post("/form", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "Medium"
    })

    expected_msg = {'description': 'Happening right now', 'title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url2)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

def test_priority_form_queue_3(sqs_client):
    set_environment_variables()
    queue3 = sqs_client.create_queue(QueueName='queue3')

    queue_url3 = queue3['QueueUrl']

    # override function global URL variable
    main.P3_QUEUE = queue_url3

    client = app.test_client()
    client.post("/form", data={
        "title": "Bug",
        "description": "Happening right now",
        "priority": "Low"
    })

    expected_msg = {'description': 'Happening right now', 'title': 'Bug'}
    sqs_messages = sqs_client.receive_message(QueueUrl=queue_url3)
    message = sqs_messages.get('Messages')[0]
    assert json.loads(message['Body']) == expected_msg

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200