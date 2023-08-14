import asyncio

from celery import Celery

from menu_app.admin_utils.main_admin import start_sync

celery = Celery('tasks')


@celery.task
def sync_data():
    asyncio.run(start_sync())
