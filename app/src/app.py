from flask import Flask, jsonify, render_template, request, redirect, url_for

from flask_restful import Api

from datetime import datetime

from log import logger

from models.task import TaskModel, TaskSchema

from database import init_db

from apis.hoge import HogeListAPI, HogeAPI

from database import db

#from taskExe import TaskExec

def create_app():

  app = Flask(__name__)
  app.config.from_object('config.Config')

  init_db(app)

  api = Api(app)
  api.add_resource(HogeListAPI, '/hoges')
  api.add_resource(HogeAPI, '/hoges/<id>')

  return app


app = create_app()

@app.route('/test', methods=["GET"])
def hello():
    logMsg = "open test index page."
    logger.warning(logMsg)
    from datetime import datetime
    return "hello, " + datetime.now().strftime('%Y/%m/%d %H:%M:%S')

@app.route('/', methods=["GET"])
def index():
    task = TaskModel.query.all()

    if not task:
      logMsg = "in index page:query data is none : data is %s."
      logger.warning(logMsg, task)
      #logMsg = "open todo page."
      #logger.warning(logMsg)
    return render_template("index.html", allTask=task)

@app.route('/show/<int:id>', methods=["GET"])
def show(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in show task page:query data is none : data is %s."
      logger.warning(logMsg, task)

    return render_template("show.html", task=task)


@app.route('/new', methods=["GET"])
def new_task():

    return render_template("new.html")


@app.route('/create', methods=["POST"])
def create_task():

    new_task = TaskModel()
    new_task.title = request.form["title"]
    new_task.content = request.form["content"]
    new_task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    new_task.commit = 0
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('.index'))
