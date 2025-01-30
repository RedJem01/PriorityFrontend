import json
import os

import boto3
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv

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

#Make SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)

@app.route('/form', methods=["GET", "POST"])
def priority_form():
    #For drop down menu
    priorities = ['Low', 'Medium', 'High']
    if request.method == "POST":
        #Get inputs
        title = request.form["title"]
        description = request.form["description"]
        priority_match = {"High": 1, "Medium": 2, "Low": 3}
        #Get priority number
        priority = priority_match[request.form["priority"]]
        #Check title and description were entered
        if not title:
            flash('Title is required!')
            return redirect(url_for('priority_form'))
        elif not description:
            flash('Description is required!')
            return redirect(url_for('priority_form'))
        else:
            #Make SQS message body
            priority_message = json.dumps({'title': title, 'description': description})
            #Send message to each separate priority queue
            if priority == 1:
                response = sqs.send_message(
                    QueueUrl=P1_QUEUE,
                    MessageBody=priority_message
                )
            elif priority == 2:
                response = sqs.send_message(
                    QueueUrl=P2_QUEUE,
                    MessageBody=priority_message
                )
            else:
                response = sqs.send_message(
                    QueueUrl=P3_QUEUE,
                    MessageBody=priority_message
                )
            print(f'Message sent: {response["MessageId"]}')
            return redirect(url_for('priority_form'))


    return render_template("priority.html", priorities=priorities)

#Helth check for api
@app.route('/health', methods=['GET'])
def health_check():
    return 'Service is all good', 200

if __name__ == '__main__':
    app.run()


