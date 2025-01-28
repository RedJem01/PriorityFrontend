import json
import os

import boto3
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv, dotenv_values
# loading variables from .env file
load_dotenv()

app = Flask(__name__)
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION'))

@app.route('/', methods=["GET", "POST"])
def priority_form():
    priorities = ['Low', 'Medium', 'High']
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority_match = {"High": 1, "Medium": 2, "Low": 3}
        priority = priority_match[request.form["priority"]]
        if not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        else:
            priority_message = {'title': title, 'description': description}
            if priority == 1:
                response = sqs.send_message(
                    QueueUrl=os.getenv('P1_QUEUE'),
                    MessageBody=priority_message
                )
            elif priority == 2:
                response = sqs.send_message(
                    QueueUrl=os.getenv('P2_QUEUE'),
                    MessageBody=priority_message
                )
            else:
                response = sqs.send_message(
                    QueueUrl=os.getenv('P3_QUEUE'),
                    MessageBody=priority_message
                )
            print(f'Message sent: {response["MessageId"]}')
            return redirect(url_for('/'))



    return render_template("priority.html", priorities=priorities)

if __name__ == '__main__':
    app.run()