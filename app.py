from crypt import methods
from datetime import datetime
from distutils.log import debug
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

DATABASE_URI = 'sqlite:///users.db'
# DATABASE_URI = 'postgres://postgres:1941997@localhost:5432/ToDo_DB'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    details = db.Column(db.String)

    def __repr__(self):
        return f'Task("{self.name}", "{self.details}")'


@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == "GET":
        tasks = Task.query.all()

        list_tasks = []
        for task in tasks:
            task_dict = {}
            task_dict["id"] = task.id
            task_dict["name"] = task.name
            task_dict["details"] = task.details
            list_tasks.append(task_dict)

        return jsonify({
            'tasks': list_tasks
        })

    elif request.method == "POST":
        id = request.json.get("id")
        name = request.json.get("name")
        details = request.json.get("details")

        # data = json.loads(request.data)
        # id = data['id']
        # name = data['name']
        # details = data['details']

        task = Task(id=id, name=name, details=details)
        # import ipdb; ipdb.set_tracr()
        # print(task)
        db.session.add(task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": f"{name} task added successfully!"
        }), 201


@app.route('/task/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def update_task(id):
    task = Task.query.filter_by(id=id).first()
    if request.method == 'GET':
        task_dict = {}
        task_dict["id"] = task.id
        task_dict["name"] = task.name
        task_dict["details"] = task.details

        return jsonify({
            'tasks': task_dict
        })

    if request.method == 'PUT':
        task.name = request.json.get('name')
        task.details = request.json.get('details')

        db.session.commit()
        return jsonify({
            "status": "success",
            "data": "task updated successfully!"
        })

    
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": "task deleted successfully!"
        })

@app.route("/")
def home():
    return "Hello, Flask!"


db.create_all()
app.run(debug=True, port=5005)