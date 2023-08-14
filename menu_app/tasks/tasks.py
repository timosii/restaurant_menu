import asyncio

from celery import Celery

from menu_app.admin_utils.parser import form_chunks
from menu_app.admin_utils.send_data import (
    send_dish_data,
    send_menu_data,
    send_submenu_data,
)
from menu_app.config import settings

user = settings.RABBITMQ_DEFAULT_USER
password = settings.RABBITMQ_DEFAULT_PASS
host = settings.RABBITMQ_DEFAULT_HOST


celery = Celery('tasks', broker=f'amqp://{user}:{password}@{host}:5672')


async def start_sync():
    DATA = form_chunks()
    for menu in DATA['menus']:
        await send_menu_data(menu)

    for submenu in DATA['submenus']:
        await send_submenu_data(menu_id=submenu['parent_menu_id'], submenu_data=submenu)

    for dish in DATA['dishes']:
        await send_dish_data(menu_id=dish['parent_menu_id'],
                             submenu_id=dish['parent_submenu_id'],
                             dish_data=dish)


@celery.task
def sync_data():
    asyncio.run(start_sync())


celery.conf.beat_schedule = {
    'sync': {
        'task': 'menu_app.tasks.tasks.sync_data',
        'schedule': 15.0,
    },
}


if __name__ == '__main__':
    sync_data()
