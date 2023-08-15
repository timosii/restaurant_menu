from celery import Celery

from menu_app.config import settings

user = settings.RABBITMQ_DEFAULT_USER
password = settings.RABBITMQ_DEFAULT_PASS
host = settings.RABBITMQ_DEFAULT_HOST
port = settings.RABBITMQ_DEFAULT_PORT
delay = settings.TIME_CELERY_DELAY

celery = Celery('tasks', broker=f'amqp://{user}:{password}@{host}:{port}')
