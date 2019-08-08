from datetime import datetime

from flask_marshmallow import Marshmallow

from flask_marshmallow.fields import fields

from sqlalchemy_utils import UUIDType

from src.database import db

import uuid

ma = Marshmallow()


class TaskModel(db.Model):
  __tablename__ = 'task'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), nullable=False)
  explain = db.Column(db.String(255), nullable=False)
  detail = db.Column(db.String(255), nullable=False)

  createTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updateTime = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

  def __init__(self, name, explain):
    self.name = name
    self.explain = explain

  #def __repr__(self):
  #  return '<TaskModel {}:{}>'.format(self.id, self.name)


class TaskSchema(ma.ModelSchema):
  class Meta:
    model = TaskModel

  createTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
  updateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
