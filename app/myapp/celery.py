from celery import Celery


def make_celery(flask_app):
    """Создает и конфигурирует task manager celery."""

    celery = Celery(
        flask_app.import_name,
        broker=flask_app.config['CELERY_BROKER_URL'],
        include=flask_app.config['CELERY_TASK_LIST']
    )

    celery.conf.update(flask_app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery