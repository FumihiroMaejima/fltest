from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.task import TaskModel, TaskSchema
from database import db
from app import app



class TaskExec():
  def __init__(self):
    super(TaskExec, self).__init__()

  @app.route('/test')
  def indexTest(self):
      # posts = Post.query.all()
      task = TaskModel.query.all()
      return render_template("index.html", allTask = task)
