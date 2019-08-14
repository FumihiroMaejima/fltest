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


Config = DevelopmentConfig
