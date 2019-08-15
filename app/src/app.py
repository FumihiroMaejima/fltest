from flask import Flask, render_template, request, redirect, url_for

from datetime import datetime

from log import logger

from models.task import TaskModel, TaskSchema

from database import init_db

from database import db

#from taskExe import TaskExec

def create_app():

  app = Flask(__name__)
  app.config.from_object('config.Config')

  init_db(app)

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
      return redirect(url_for('.index'))

    return render_template("task/show.html", task=task)


@app.route('/new', methods=["GET"])
def new_task():
    return render_template("task/new.html")


@app.route('/create_confirm', methods=["POST"])
def create_confirm():

    task_title = request.form["title"]
    task_content = request.form["content"]

    if not task_title:
      logMsg = "in create task confirm page:task title is none : task title is %s."
      logger.warning(logMsg, task_title)

    return render_template("task/create_confirm.html", task_title=task_title, task_content=task_content)


@app.route('/create', methods=["POST"])
def create_task():

    req_title = request.form["title"]
    req_content = request.form["content"]
    new_task = TaskModel(req_title, req_content)
    #new_task.title = request.form["title"]
    #new_task.content = request.form["content"]
    new_task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    new_task.commit = 0
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/edit/<int:id>', methods=["GET"])
def edit_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in edit task page:query data is none : data is %s."
      logger.warning(logMsg, task)

    return render_template("task/edit.html", task=task)


@app.route('/update_confirm/<int:id>', methods=["POST"])
def update_confirm(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in update task execution:query data is none : data is %s."
      logger.warning(logMsg, task)

    task_title = request.form["title"]
    task_content = request.form["content"]

    if not task_title:
      logMsg = "in create task confirm page:task title is none : task title is %s."
      logger.warning(logMsg, task_title)

    return render_template("task/update_confirm.html", task=task, task_title=task_title, task_content=task_content)


@app.route('/update/<int:id>', methods=["POST"])
def update_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in update task execution:query data is none : data is %s."
      logger.warning(logMsg, task)

    task.title = request.form["title"]
    task.content = request.form["content"]
    task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/complete/<int:id>', methods=["POST"])
def complete_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in complete_task execution:query data is none : data is %s."
      logger.warning(logMsg, task)

    task.commit = 1
    task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/incomplete/<int:id>', methods=["POST"])
def incomplete_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in incomplete_task execution:query data is none : data is %s."
      logger.warning(logMsg, task)

    task.commit = 0
    task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in delete execution:query data is none : data is %s."
      logger.warning(logMsg, task)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/delete/allcomplete', methods=["POST"])
def delete_allcomplete():
    complete_task = TaskModel.query.filter_by(commit=1).all()

    if not complete_task:
      logMsg = "in delete complete_task execution:query data is none : data is %s."
      logger.warning(logMsg, complete_task)

    for i in complete_task:
      db.session.delete(i)
      db.session.commit()

    return redirect(url_for('.index'))
