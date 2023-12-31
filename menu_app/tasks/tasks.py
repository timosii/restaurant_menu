import asyncio

from menu_app.admin_utils.parser import form_data
from menu_app.admin_utils.send_data import (
    send_dish_data,
    send_menu_data,
    send_submenu_data,
)
from menu_app.tasks.config_celery import celery, delay


async def start_sync() -> None:
    DATA = form_data()
    for menu in DATA['menus']:
        await send_menu_data(menu_data=menu)

    for submenu in DATA['submenus']:
        await send_submenu_data(menu_id=submenu['parent_menu_id'], submenu_data=submenu)

    for dish in DATA['dishes']:
        await send_dish_data(menu_id=dish['parent_menu_id'],
                             submenu_id=dish['parent_submenu_id'],
                             dish_data=dish)
    return


@celery.task
def sync_data() -> None:
    asyncio.run(start_sync())
    return None


celery.conf.beat_schedule = {
    'sync': {
        'task': 'menu_app.tasks.tasks.sync_data',
        'schedule': delay,
    },
}
