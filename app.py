from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class PlanModel(db.Model):
    __tablename__ = 'planmodel'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    main_objective = db.Column(db.String)
    task_list = db.relationship('TaskModel', backref='plan', lazy=True)


    def __init__(self, title, main_objective, task_list):
        self.title = title
        self.main_objective = main_objective
        self.task_list = task_list

class PlanSchema(ma.Schema):
    class Meta:
        fields = ("title", "main_objective", "task_list")



class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('planmodel.id'), primary_key=True)

    def __init__(self, task, plan_id):
        self.task = task
        self.plan_id = plan_id

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("task", "plan_id")

task_schema = TaskSchema
tasks_schema = TaskSchema(many=True)
plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)



@app.route('/plans')
def plan_list():
    all_plans = PlanModel.query.all()
    return jsonify(plans_schema.dump(all_plans))

@app.route('/plan/task/new', methods=['POST'])
def create_task():
    task = request.json.get('task')
    plan_id = request.json.get('plan_id')

    newTask = (task, plan_id)

    db.session.add(newTask)
    db.session.commit()

    return task_schema.jsonify(newTask)

@app.route('/plan/new', methods=['POST'])
def create_plan():
    title = request.json.get('title')
    main_objective = request.json.get('main_objective')
    task_list = request.json.get('task_list')

    plan = PlanModel(title, main_objective, task_list)

    db.session.add(plan)
    db.session.commit()

    return plan_schema.jsonify(plan)















# @app.route("/plan/new", methods=["POST"])
# def add_plan():
#     if request.content_type != "application/json":
#         return jsonify("JSON pls")

#     post_data = request.get_json()
#     project_name = post_data.get("project_name")
#     main_objective = post_data.get("main_objective")

#     new_record = Plans(project_name, main_objective)
#     db.session.add(new_record)
#     db.session.commit()

#     return jsonify("Plan added successfully")


# @app.route("/plans/get", methods=["GET"])
# def get_plans():
#     records = db.session.query(Plans).all()
#     return jsonify(plans_schema)
 



if __name__ == "__main__":
    app.run(debug=True)