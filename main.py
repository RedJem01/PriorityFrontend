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

@app.route('/form', methods=["GET", "POST"])
def priority_form():
    print(AWS_REGION)
    try:
        # Make SQS client
        sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY
        )
        #For drop down menu
        priorities = ['Low', 'Medium', 'High']
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

#Health check for api
@app.route('/', methods=['GET'])
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run()


