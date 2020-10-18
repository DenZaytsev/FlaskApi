import os
import redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """Настройки нашего Flask приложения."""

    SELF_SERVER = "python"
    SELF_SERVER_PORT = 8080
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = bool(os.environ.get("DEBUG", default=0))

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL')

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(REDIS_URL)

    CELERY_BROKER_URL = REDIS_URL
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_TASK_LIST = [
        'tasks.tasks',
        'tasks.scheduler'
    ]
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERYBEAT_SCHEDULE = {

    }

