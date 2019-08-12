from flask import Flask, jsonify, render_template

from flask_restful import Api

from log import logger

from models.task import TaskModel, TaskSchema

from database import init_db

from apis.hoge import HogeListAPI, HogeAPI

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

@app.route('/', methods=["GET"])
def hello():
    logMsg = "open index page."
    logger.warning(logMsg)
    from datetime import datetime
    return "hello, " + datetime.now().strftime('%Y/%m/%d %H:%M:%S')

@app.route('/test', methods=["GET"])
def indexTest():
    task = TaskModel.query.all()

    if not task:
      logMsg = "query data is none : data is %s."
      logger.warning(logMsg, task)
      #logMsg = "open todo page."
      #logger.warning(logMsg)
    return render_template("index.html", allTask = task)
