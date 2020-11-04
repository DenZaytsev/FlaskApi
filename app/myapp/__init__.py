from flask import Flask
from flask_redis import FlaskRedis
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .celery import make_celery
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
flask_session = Session(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_size=100, max_overflow=10, convert_unicode=True)
DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_global_session = DbSession()

celery = make_celery(app)

redis = FlaskRedis(app)


