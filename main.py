import json
import os

import boto3
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
from loguru import logger

# loading variables from .env file
load_dotenv()
AWS_REGION = os.getenv('AWS_REGION')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
P1_QUEUE = os.getenv('P1_QUEUE')
P2_QUEUE = os.getenv('P2_QUEUE')
P3_QUEUE = os.getenv('P3_QUEUE')

app = Flask(__name__)
app.secret_key = 'the random string'

@app.route('/', methods=["GET", "POST"])
def priority_form():
    # For drop down menu
    priorities = ['Low', 'Medium', 'High']
    try:
        # Make SQS client
        sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY
        )

        if request.method == "POST":

            #Get inputs
            title = request.form["title"]
            description = request.form["description"]
            #Get priority number
            priority = request.form["priority"]

            #Check title and description were entered
            if not title:
                flash('Title is required!')
                logger.warning("Title not on POST request")
                return redirect(url_for('priority_form'))

            elif not description:
                flash('Description is required!')
                logger.warning("Title not on POST request")
                return redirect(url_for('priority_form'))

            else:
                response_text = bedrock_suggestion(title, description)
                description += "\n\n Suggested fix: \n\n" + response_text
                #Make SQS message body
                priority_message = json.dumps({'title': title, 'description': description})
                #Send message to each separate priority queue
                if priority == "High":
                    logger.info(f"SQS message sent to priority queue 1 with message: {priority_message}")
                    response = sqs.send_message(
                        QueueUrl=P1_QUEUE,
                        MessageBody=priority_message
                    )
                elif priority == "Medium":
                    logger.info(f"SQS message sent to priority queue 2 with message: {priority_message}")
                    response = sqs.send_message(
                        QueueUrl=P2_QUEUE,
                        MessageBody=priority_message
                    )
                else:
                    logger.info(f"SQS message sent to priority queue 3 with message: {priority_message}")
                    response = sqs.send_message(
                        QueueUrl=P3_QUEUE,
                        MessageBody=priority_message
                    )
                return redirect(url_for('priority_form'))
    except Exception as e:
        logger.error(f"An error occurred: {e}")


    return render_template("priority.html", priorities=priorities)

def bedrock_suggestion(title, description):
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION
    )
    model_id = "amazon.titan-text-express-v1"
    user_message = f"Provide a suggestion for fixing this bug without asking for more information: {title} and has a description of: {description}"
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]
    bedrock_response = bedrock.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )
    return bedrock_response["output"]["message"]["content"][0]["text"]

#Health check for api
@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run()