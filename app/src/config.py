import os


class DevelopmentConfig:

  # SQLAlchemy
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
      **{
          'user': os.getenv('DB_USER', 'test'),
          'password': os.getenv('DB_PASSWORD', 'test'),
          'host': os.getenv('DB_HOST', 'test'),
          'database': os.getenv('DB_DATABASE', 'test'),
      })
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False
  APP_URL = os.getenv('APP_URL', 'test')
  SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


Config = DevelopmentConfig
