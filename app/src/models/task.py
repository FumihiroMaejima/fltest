from datetime import datetime

from flask_marshmallow import Marshmallow

from flask_marshmallow.fields import fields

from sqlalchemy_utils import UUIDType

from database import db

import uuid

ma = Marshmallow()


class TaskModel(db.Model):
  __tablename__ = 'task'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Text())
  title = db.Column(db.Text())
  content = db.Column(db.Text())
  commit = db.Column(db.Integer())

  createTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updateTime = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

  def __init__(self, title, content):
    self.title = title
    self.content = content

  def __repr__(self):
    return '<TaskModel ' + str(self.id) + ':' + self.title + '>'


class TaskSchema(ma.ModelSchema):
  class Meta:
    model = TaskModel

  createTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
  updateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
