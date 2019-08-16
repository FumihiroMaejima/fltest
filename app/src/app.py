from flask import Flask, render_template, request, redirect, url_for, session, abort

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

app.secret_key = app.config['SECRET_KEY']


# error handling start
def user_bad_request(error):
    return render_template('errors/400.html'), 400


def user_request_forbidden(error):
    return render_template('errors/403.html'), 403


def page_not_found(error):
    return render_template('errors/404.html'), 404


def request_method_not_allowed(error):
    return render_template('errors/405.html'), 405


app.register_error_handler(400, user_bad_request)
app.register_error_handler(403, user_request_forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(405, request_method_not_allowed)
# error handling end


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
      abort(404)

    return render_template("task/show.html", task=task)


@app.route('/new', methods=["GET"])
def new_task():

    referer_page = request.headers.get("Referer")
    index_page = app.config['APP_URL'] + '/'

    if referer_page == index_page:
      session_title = ''
      session_content = ''
      session['title'] = ''
      session['content'] = ''
    elif 'title' in session and 'content' in session:
      session_title = session.get('title')
      session_content = session.get('content')
    else:
        abort(400)

    return render_template("task/new.html", session_title=session_title, session_content=session_content)


@app.route('/create_confirm', methods=["POST"])
def create_confirm():

    task_title = request.form["title"]
    task_content = request.form["content"]

    if not task_title:
      logMsg = "in create task confirm page:task title is none : task title is %s."
      logger.warning(logMsg, task_title)
      abort(400)

    if 'title' not in session and 'content' not in session:
      abort(400)
    else:
      session['title'] = task_title
      session['content'] = task_content

    return render_template("task/create_confirm.html", task_title=task_title, task_content=task_content)


@app.route('/create', methods=["POST"])
def create_task():
    session_title = session.get('title')
    session_content = session.get('content')

    post_title = request.form["title"]
    post_content = request.form["content"]
    if session_title != post_title or session_content != post_content:
      logMsg = "in create task execution: input data is wrong : post data is %s."
      logger.warning(logMsg, post_title)
      abort(400)

    new_task = TaskModel(session_title, session_content)
    #new_task.title = request.form["title"]
    #new_task.content = request.form["content"]
    new_task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    new_task.commit = 0
    db.session.add(new_task)
    db.session.commit()

    session.pop('title', None)
    session.pop('content', None)

    return redirect(url_for('.index'))


@app.route('/edit/<int:id>', methods=["GET"])
def edit_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in edit task page:query data is none : data is %s."
      logger.warning(logMsg, task)
      abort(404)

    referer_page = request.headers.get("Referer")
    detail_page = app.config['APP_URL'] + '/show/' + str(task.id)

    if referer_page == detail_page:
      session['edit_title'] = ''
      session['edit_content'] = ''
    elif 'edit_title' in session and 'edit_content' in session:
      task.title = session.get('edit_title')
      task.content = session.get('edit_content')
    else :
        abort(400)

    return render_template("task/edit.html", task=task)


@app.route('/update_confirm/<int:id>', methods=["POST"])
def update_confirm(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in update task execution:query data is none : data is %s."
      logger.warning(logMsg, task)
      abort(400)

    task_title = request.form["title"]
    task_content = request.form["content"]

    if not task_title:
      logMsg = "in create task confirm page:task title is none : task title is %s."
      logger.warning(logMsg, task_title)
      abort(400)

    if 'edit_title' not in session and 'edit_content' not in session:
        abort(400)
    else:
      session['edit_title'] = task_title
      session['edit_content'] = task_content

    return render_template("task/update_confirm.html", task=task, task_title=task_title, task_content=task_content)


@app.route('/update/<int:id>', methods=["POST"])
def update_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in update task execution:query data is none : data is %s."
      logger.warning(logMsg, task)
      abort(400)

    session_title = session.get('edit_title')
    session_content = session.get('edit_content')
    post_title = request.form["title"]
    post_content = request.form["content"]

    if session_title != post_title or session_content != post_content:
      logMsg = "in update task execution: input data is wrong : post data is %s."
      logger.warning(logMsg, post_title)
      abort(400)

    task.title = post_title
    task.content = post_content
    task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    session.pop('edit_title', None)
    session.pop('edit_content', None)

    return redirect(url_for('.index'))


@app.route('/complete/<int:id>', methods=["POST"])
def complete_task(id):
    task = TaskModel.query.get(id)

    if not task:
      logMsg = "in complete_task execution:query data is none : data is %s."
      logger.warning(logMsg, task)
      abort(400)

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
      abort(400)

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
      abort(400)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/delete/allcomplete', methods=["POST"])
def delete_allcomplete():
    complete_task = TaskModel.query.filter_by(commit=1).all()

    if not complete_task:
      logMsg = "in delete complete_task execution:query data is none : data is %s."
      logger.warning(logMsg, complete_task)
      abort(400)

    for i in complete_task:
      db.session.delete(i)
      db.session.commit()

    return redirect(url_for('.index'))
