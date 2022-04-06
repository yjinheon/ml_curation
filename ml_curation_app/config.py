import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
""" 
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY 관련 ref
- https://www.delftstack.com/ko/howto/python/set-and-get-environment-variables-in-python/
os.getenv(x)함수는 환경 변수x의 값을 포함하는 문자열 변수를 반환

import os

os.environ["My Environment"] = "The Best Environment"
myenv = os.getenv("My Environment")

print(myenv)
---

이 파일은 __init__ 파일에서 dict파일을 불러오는 식으로 사용한다.

from .config import config_by_name

"""

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ngle_api_tongchun')
    DEBUG = False
    db = {
    'dbuser': 'bphsqwgb',
    'dbpass': 'SEjljOwNYmVgkmqFSips-tzVWsBf5tKY',
    'dbhost': 'otto.db.elephantsql.com',
    'port': 3306,
    'dbname': 'bphsqwgb'
    }
    database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=db['dbuser'],
    dbpass=db['dbpass'],
    dbhost=db['dbhost'],
    dbname=db['dbname']
    )

class DevConfig(Config):
	# uncomment the line below to use postgres
	# SQLALCHEMY_DATABASE_URI = elephantsql
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = Config.database_uri
	SQLALCHEMY_TRACK_MODIFICiATIONS = False

config_by_name = dict(
	dev=DevConfig
    )

key = Config.SECRET_KEY
