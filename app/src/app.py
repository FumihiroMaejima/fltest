from flask import Flask, render_template, request, redirect, url_for, session, abort

from datetime import datetime

from flask_wtf import FlaskForm

from flask_wtf.csrf import CSRFProtect, CSRFError

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from log import logger

from models.task import TaskModel, TaskSchema

from models.user import UserModel

from database import init_db

from database import db

from blog_form import BlogForm

from loginForm import loginForm

from createUserForm import createUserForm

from taskform import TaskForm

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_db(app)

    return app


app = create_app()

app.secret_key = app.config['SECRET_KEY']

login_manager = LoginManager()

login_manager.init_app(app)

csrf = CSRFProtect(app)

if app.config['ENV'] == 'production':
    app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')

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


def delete_user_create_session():
    if 'name' in session:
        session.pop('title', None)
    if 'email' in session:
        session.pop('content', None)
    if 'password' in session:
        session.pop('password', None)
    if 'user_create_csrf_token' in session:
        session.pop('user_create_csrf_token', None)


def delete_create_session():
    if 'title' in session:
        session.pop('title', None)
    if 'content' in session:
        session.pop('content', None)
    if 'create_csrf_token' in session:
        session.pop('create_csrf_token', None)


def delete_task_validation_session():
    if 'title_null_check_msg' in session:
        session.pop('title_null_check_msg', None)
    if 'title_validation_msg' in session:
        session.pop('title_validation_msg', None)
    if 'content_validation_msg' in session:
        session.pop('content_validation_msg', None)

def delete_edit_session():
    if 'edit_task_id' in session:
        session.pop('edit_task_id', None)
    if 'edit_title' in session:
        session.pop('edit_title', None)
    if 'edit_content' in session:
        session.pop('edit_content', None)
    if 'edit_csrf_token' in session:
        session.pop('edit_csrf_token', None)


@app.route('/test', methods=["GET"])
def hello():
    logMsg = "open test index page."
    logger.warning(logMsg)
    from datetime import datetime
    return "hello, " + datetime.now().strftime('%Y/%m/%d %H:%M:%S')


@app.route("/testform", methods=["GET", "POST"])
def indexform():
    form = BlogForm()
    if request.method == "GET":
        message = "フォームを送ってみよう！！"
        return render_template("testform.html", form=form, message=message)

    if request.method == "POST":
        if form.validate_on_submit():
            message = "バリデーションを通ったよ＼(^o^)／"
            return render_template("testform.html", form=form, message=message)

        message = "バリデーションに失敗したよ(T_T)"
        return render_template("testform.html", form=form, message=message)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

# 未認証の際のリダイレクト先を設定
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('.login_index'))


@app.route('/login', methods=["GET", "POST"])
def login_index():
    form = loginForm()

    if request.method == 'POST' and form.validate_on_submit():
        session['login_csrf_token'] = request.form["login_csrf_token"]

        user, authenticated = UserModel.auth(db.session.query, form.email.data, form.password.data)

        user_id = user.id
        if user_id == None:
          logMsg = "in login execution: user_id is %s."
          logger.warning(logMsg, user)
          return render_template("auth/login.html", form=form)

        if authenticated:
            login_user(user)
            return redirect(url_for('.index'))
        else:
            return render_template("auth/login.html", form=form)
    else:
        return render_template("auth/login.html", form=form)


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    request_token = request.form["login_csrf_token"]
    session_token = session.get('login_csrf_token')

    if request_token != session_token:
        logMsg = "in logout execution: token is wrong. token is %s."
        logger.warning(logMsg, request_token)
        abort(400)
    else:
        session.pop('login_csrf_token', None)

    logout_user()
    return redirect(url_for('.login_index'))


def create_user():
    form = createUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        session['user_create_csrf_token'] = request.form["user_create_csrf_token"]
        session['name'] = request.form["name"]
        session['email'] = request.form["email"]
        session['password'] = request.form["password"]
        return redirect(url_for('.create_user_confirm'))
    else:
        return render_template("auth/new.html", form=form)


@app.route('/user/create/confirm', methods=["GET"])
@login_required
def create_user_confirm():

    if 'user_create_csrf_token' not in session:
        logMsg = "in create user confirm execution:csrf token session is none."
        logger.warning(logMsg)
        abort(400)

    if 'name' not in session or 'name' not in session or 'email' not in session or 'password' not in session:
        logMsg = "in create user confirm execution:session data is wrong."
        logger.warning(logMsg)
        abort(400)

    session_token = session.get('user_create_csrf_token')
    session_name = session.get('name')
    session_email = session.get('email')
    session_password = session.get('password')

    pass_length = len(session_password)
    num = 1
    mask_password = "●"
    while num < pass_length:
        mask_password = mask_password + "●"
        num+=1

    return render_template("auth/create_confirm.html", session_token=session_token, session_name=session_name, session_email=session_email, session_password=session_password, mask_password=mask_password)


@app.route('/user/create/exec', methods=["POST"])
@login_required
def create_user_exec():
    session_token = session.get('user_create_csrf_token')
    session_name = session.get('name')
    session_email = session.get('email')
    session_password = session.get('password')

    request_token = request.form["user_create_csrf_token"]
    request_name = request.form["name"]
    request_email = request.form["email"]
    request_password = request.form["password"]

    if session_token != request_token:
        logMsg = "in create user execution:csrf token is wrong."
        logger.warning(logMsg)
        abort(400)

    if session_name != request_name or session_email != request_email or session_password != request_password:
        logMsg = "in create user execution:request data is wrong."
        logger.warning(logMsg)
        abort(400)

    try:
        new_user = UserModel(session_email)
        new_user.name = session_name
        new_user.password = session_password
        new_user.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        db.session.add(new_user)
        db.session.commit()

        delete_user_create_session()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in create user executionn: crate execution is failed. please return index page."
        logger.warning(logMsg)
        delete_user_create_session()
        abort(400)


@app.route('/', methods=["GET"])
@login_required
def index():
    delete_create_session()
    delete_edit_session()
    delete_task_validation_session()
    delete_user_create_session()

    if 'login_csrf_token' not in session:
        abort(400)
    login_token = session.get('login_csrf_token')


    task = TaskModel.query.all()

    if not task:
        logMsg = "in index page:query data is none : data is %s."
        logger.warning(logMsg, task)

    return render_template("index.html", login_token=login_token, allTask=task)


@app.route('/show/<int:id>', methods=["GET"])
@login_required
def show(id):
    task = TaskModel.query.get(id)

    if not task:
        logMsg = "in show task page:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(404)

    return render_template("task/show.html", task=task)


@app.route('/new', methods=["GET"])
@login_required
def new_task():
    validation_msg = {"title_require":'', "title_length":'', "content_length":''}
    referer_page = request.headers.get("Referer")
    index_page = app.config['APP_URL'] + '/'

    if referer_page == index_page:
        session_title = ''
        session_content = ''
        create_session_token = ''
        session['title'] = ''
        session['content'] = ''
        session['create_csrf_token'] = ''
    elif 'title' in session and 'content' in session and 'create_csrf_token' in session:
        session_title = session.get('title')
        session_content = session.get('content')
        create_session_token = session.get('create_csrf_token')
        if 'title_null_check_msg' in session or 'title_validation_msg' in session or 'content_validation_msg' in session:
            validation_msg["title_require"] = session['title_null_check_msg']
            validation_msg["title_length"] = session['title_validation_msg']
            validation_msg["content_length"] = session['content_validation_msg']
            delete_task_validation_session()
    else:
        abort(400)

    return render_template("task/new.html", validation_msg=validation_msg, session_title=session_title, session_content=session_content, create_session_token=create_session_token)


@app.route('/create_confirm', methods=["POST"])
@login_required
def create_confirm():
    task_title = request.form["title"]
    task_content = request.form["content"]
    create_session_token = request.form["create_csrf_token"]

    task_form = TaskForm(task_title, task_content)
    title_null_check_msg = task_form.title_require()
    title_validation_msg = task_form.title_length()
    content_validation_msg = task_form.content_length()
    #validation_msg = {"title_require":title_null_check_msg, "title_length":title_validation_msg, "content_length":content_validation_msg}

    if title_null_check_msg != '' or title_validation_msg != '' or content_validation_msg != '':
        session['title'] = task_title
        session['content'] = task_content
        session['create_csrf_token'] = create_session_token
        session['title_null_check_msg'] = title_null_check_msg
        session['title_validation_msg'] = title_validation_msg
        session['content_validation_msg'] = content_validation_msg
        #return render_template("task/new.html", validation_msg=validation_msg, session_title=task_title, session_content=task_content, create_session_token=create_session_token)
        return redirect(url_for('.new_task'))

    if not task_title:
        logMsg = "in create task confirm page:task title is none : task title is %s."
        logger.warning(logMsg, task_title)
        abort(400)

    if 'title' not in session and 'content' not in session:
        abort(400)
    else:
        session['title'] = task_title
        session['content'] = task_content
        session['create_csrf_token'] = create_session_token

    return render_template("task/create_confirm.html", task_title=task_title, task_content=task_content, create_session_token=create_session_token)


@app.route('/create', methods=["POST"])
@login_required
def create_task():
    session_title = session.get('title')
    session_content = session.get('content')
    session_token = session.get('create_csrf_token')

    post_title = request.form["title"]
    post_content = request.form["content"]
    create_csrf_token = request.form["create_csrf_token"]

    if create_csrf_token != session_token:
        logger.warning('create csrf_token is %s ', create_csrf_token)
        abort(400)

    if session_title != post_title or session_content != post_content:
        logMsg = "in create task execution: input data is wrong : post data is %s."
        logger.warning(logMsg, post_title)
        abort(400)

    try:
        new_task = TaskModel(session_title, session_content)
        #new_task.title = request.form["title"]
        #new_task.content = request.form["content"]
        new_task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        new_task.commit = 0
        db.session.add(new_task)
        db.session.commit()

        delete_create_session()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in crate task execution: crate execution is failed. please return index page."
        logger.warning(logMsg)
        delete_create_session()
        abort(400)


@app.route('/edit/<int:id>', methods=["GET"])
@login_required
def edit_task(id):
    validation_msg = {"title_require":'', "title_length":'', "content_length":''}
    task = TaskModel.query.get(id)

    if not task:
        logMsg = "in edit task page:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(404)

    referer_page = request.headers.get("Referer")
    detail_page = app.config['APP_URL'] + '/show/' + str(task.id)

    if referer_page == detail_page:
        session['edit_task_id'] = task.id
        session['edit_title'] = ''
        session['edit_content'] = ''
        session['edit_csrf_token'] = ''
        edit_session_token = ''
    elif 'edit_task_id' in session and 'edit_title' in session and 'edit_content' in session and 'edit_csrf_token' in session:
        if task.id != session.get('edit_task_id'):
            logMsg = "in edit task page: id is wrong : query id is %s."
            logger.warning(logMsg, task.id)
            abort(400)
        task.title = session.get('edit_title')
        task.content = session.get('edit_content')
        edit_session_token = session.get('edit_csrf_token')
        if 'title_null_check_msg' in session or 'title_validation_msg' in session or 'content_validation_msg' in session:
            validation_msg["title_require"] = session['title_null_check_msg']
            validation_msg["title_length"] = session['title_validation_msg']
            validation_msg["content_length"] = session['content_validation_msg']
            delete_task_validation_session()
    else :
        abort(400)

    return render_template("task/edit.html", validation_msg=validation_msg, task=task, edit_session_token=edit_session_token)


@app.route('/update_confirm/', methods=["POST"])
@login_required
def update_confirm():
    post_task_id = request.form["task_id"]
    task_title = request.form["title"]
    task_content = request.form["content"]
    edit_session_token = request.form["edit_csrf_token"]
    session_task_id = session.get('edit_task_id')

    if post_task_id != str(session_task_id):
        logMsg = "in update task confirm execution:post data is wrong : request post_task_id is %s."
        logger.warning(logMsg, post_task_id)
        abort(400)

    task = TaskModel.query.get(post_task_id)

    task_form = TaskForm(task_title, task_content)
    title_null_check_msg = task_form.title_require()
    title_validation_msg = task_form.title_length()
    content_validation_msg = task_form.content_length()
    #validation_msg = {"title_require":title_null_check_msg, "title_length":title_validation_msg, "content_length":content_validation_msg}

    if title_null_check_msg != '' or title_validation_msg != '' or content_validation_msg != '':
        session['edit_title'] = task_title
        session['edit_content'] = task_content
        session['edit_csrf_token'] = edit_session_token
        session['title_null_check_msg'] = title_null_check_msg
        session['title_validation_msg'] = title_validation_msg
        session['content_validation_msg'] = content_validation_msg
        #return render_template("task/edit.html", validation_msg=validation_msg, task=task, edit_session_token=edit_session_token)
        return redirect(url_for('.edit_task', id=session_task_id))


    if not task:
        logMsg = "in update task confirm execution:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(400)

    if not task_title:
        logMsg = "in update task confirm execution:task title is none : task title is %s."
        logger.warning(logMsg, task_title)
        abort(400)

    if 'edit_task_id' not in session or 'edit_title' not in session or 'edit_content' not in session:
        abort(400)
    else:
        session['edit_title'] = task_title
        session['edit_content'] = task_content
        session['edit_csrf_token'] = edit_session_token

    return render_template("task/update_confirm.html", task_id=session_task_id, task_title=task_title, task_content=task_content, edit_session_token=edit_session_token)


@app.route('/update/', methods=["POST"])
@login_required
def update_task():
    session_task_id = session.get('edit_task_id')
    session_title = session.get('edit_title')
    session_content = session.get('edit_content')
    session_token = session.get('edit_csrf_token')
    post_task_id = request.form["task_id"]
    post_title = request.form["title"]
    post_content = request.form["content"]
    edit_csrf_token = request.form["edit_csrf_token"]

    if edit_csrf_token != session_token:
        logger.warning('edit csrf_token is %s ', edit_csrf_token)
        abort(400)

    task = TaskModel.query.get(post_task_id)

    if not task:
        logMsg = "in update task execution:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(400)

    if post_task_id != str(session_task_id):
        logMsg = "in update task execution:post data is wrong : request post_task_id  is %s."
        logger.warning(logMsg, post_task_id)
        abort(400)

    if session_title != post_title or session_content != post_content:
        logMsg = "in update task execution: input data is wrong : post data is %s."
        logger.warning(logMsg, post_title)
        abort(400)

    try:
        task.title = post_title
        task.content = post_content
        task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        db.session.commit()

        delete_edit_session()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in update task execution: update execution is failed. please return index page."
        logger.warning(logMsg)

        delete_edit_session()
        abort(400)


@app.route('/complete/<int:id>', methods=["POST"])
@login_required
def complete_task(id):
    complete_csrf_token = request.form["complete_csrf_token"]

    if not complete_csrf_token or complete_csrf_token == '':
        logMsg = "in complete_task execution:token is none : data is %s."
        logger.warning(logMsg, complete_csrf_token)
        abort(400)

    task = TaskModel.query.get(id)

    if not task:
        logMsg = "in complete_task execution:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(400)

    try:
        task.commit = 1
        task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        db.session.commit()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in complete task execution: complete execution is failed. please return index page."
        logger.warning(logMsg)
        abort(400)


@app.route('/incomplete/<int:id>', methods=["POST"])
@login_required
def incomplete_task(id):
    incomplete_csrf_token = request.form["incomplete_csrf_token"]

    if not incomplete_csrf_token or incomplete_csrf_token == '':
        logMsg = "in incomplete_task execution:token is none : data is %s."
        logger.warning(logMsg, incomplete_csrf_token)
        abort(400)

    task = TaskModel.query.get(id)

    if not task:
        logMsg = "in incomplete_task execution:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(400)

    try:
        task.commit = 0
        task.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        db.session.commit()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in incomplete task execution: incomplete execution is failed. please return index page."
        logger.warning(logMsg)
        abort(400)


@app.route('/delete/<int:id>', methods=["POST"])
@login_required
def delete(id):
    delete_csrf_token = request.form["delete_csrf_token"]

    if not delete_csrf_token or delete_csrf_token == '':
        logMsg = "in delete_task execution:token is none : data is %s."
        logger.warning(logMsg, delete_csrf_token)
        abort(400)

    task = TaskModel.query.get(id)

    if not task:
        logMsg = "in delete execution:query data is none : data is %s."
        logger.warning(logMsg, task)
        abort(400)

    try:
        db.session.delete(task)
        db.session.commit()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in delete task execution: delete execution is failed. please return index page."
        logger.warning(logMsg)
        abort(400)


@app.route('/delete/allcomplete', methods=["POST"])
@login_required
def delete_allcomplete():
    allcomplete_delete_csrf_token = request.form["allcomplete_delete_csrf_token"]

    if not allcomplete_delete_csrf_token or allcomplete_delete_csrf_token == '':
        logMsg = "in delete complete_task execution:token is none : data is %s."
        logger.warning(logMsg, allcomplete_delete_csrf_token)
        abort(400)

    complete_task = TaskModel.query.filter_by(commit=1).all()

    if not complete_task:
        logMsg = "in delete complete_task execution:query data is none : data is %s."
        logger.warning(logMsg, complete_task)
        abort(400)

    try:
        for i in complete_task:
            db.session.delete(i)
        db.session.commit()

        return redirect(url_for('.index'))
    except:
        db.session.rollback()

        logMsg = "in delete allcomplete task execution: delete allcomplete execution is failed. please return index page."
        logger.warning(logMsg)
        abort(400)
