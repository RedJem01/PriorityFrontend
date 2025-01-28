from flask import Flask, render_template, flash, request

app = Flask(__name__)

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
            priority_message = {'title': title, 'description': description, 'priority': priority}


    return render_template("priority.html", priorities=priorities)

if __name__ == '__main__':
    app.run()