from flask import Flask

class TaskForm():
  title = None
  content = None

  def __init__(self, title, content):
    self.title = title
    self.content = content
