# Todo List Site
# James Hill, 2021

# import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    complete = db.Column(db.String(10), default='incomplete', nullable=False)


db.create_all()


# Routes
# Index
@app.route('/')
def home():
    #  READ ALL RECORDS
    all_tasks = db.session.query(Task).all()
    return render_template("index.html", tasks=all_tasks)


# Add
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_task = Task(
            text=request.form["task"],
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("/add.html")


# Complete
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Update Status
        task_id = request.form["id"]
        updated_task = Task.query.get(task_id)
        updated_task.complete = request.form["complete"]
        db.session.commit()
        return redirect(url_for("home"))
    task_id = request.args.get("id")
    task_selected = Task.query.get(task_id)
    return render_template("edit_status.html", task=task_selected)


# Delete
@app.route("/delete")
def delete():
    task_id = request.args.get('id')

    # DELETE A RECORD BY ID
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# Run Command
if __name__ == '__main__':
    app.run(debug=True)
