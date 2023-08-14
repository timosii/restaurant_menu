from uuid import UUID

import httpx

BASE_URL = 'http://localhost:8000'


async def send_menu_data(menu_data):
    url = f'{BASE_URL}/api/v1/menus/'

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=menu_data)

    if response.status_code == 201:
        return response.text
    elif response.status_code == 400:
        menu_id = menu_data['id']
        url = f'{BASE_URL}/api/v1/menus/{menu_id}'
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=menu_data)

    else:
        raise Exception(f'Error creating menu: {response.text}')


async def send_submenu_data(menu_id: UUID, submenu_data):
    url = f'{BASE_URL}/api/v1/menus/{menu_id}/submenus/'

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=submenu_data)

    if response.status_code == 201:
        return response.text
    elif response.status_code == 400:
        submenu_id = submenu_data['id']
        url = f'{BASE_URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=submenu_data)
    else:
        raise Exception(f'Error creating submenu: {response.text}')


async def send_dish_data(menu_id: UUID, submenu_id: UUID, dish_data):
    url = f'{BASE_URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/'

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dish_data)

    if response.status_code == 201:
        return response.text
    elif response.status_code == 400:
        dish_id = dish_data['id']
        url = f'{BASE_URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=dish_data)
    else:
        raise Exception(f'Error creating dish: {response.text}')
