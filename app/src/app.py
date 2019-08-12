from flask import Flask, jsonify

from flask_restful import Api

from log import logger

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

@app.route("/")
def hello():
    logMsg = "index page."
    logger.warning(logMsg)
    from datetime import datetime
    return "hello, " + datetime.now().strftime('%Y/%m/%d %H:%M:%S')
