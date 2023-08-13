import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from menu_app import models
from menu_app.database import get_db, get_url
from menu_app.main import app

DATABASE_URL_TEST = get_url()

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

models.Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope='module')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

menu = {
    'title': 'My menu 1',
    'description': 'My menu description 1'
}

menu_updated = {
    'title': 'My updated menu 1',
    'description': 'My updated menu description 1'
}

submenu = {
    'title': 'My submenu 1',
    'description': 'My submenu description 1'
}

submenu_updated = {
    'title': 'My updated submenu 1',
    'description': 'My updated submenu description 1'
}

dish_1 = {
    'title': 'My dish 1',
    'description': 'My dish description 1',
    'price': '12.50'
}

dish_updated = {
    'title': 'My updated dish 1',
    'description': 'My updated dish description 1',
    'price': '14.50'
}

dish_2 = {
    'title': 'My dish 2',
    'description': 'My dish description 2',
    'price': '13.50'
}

viewall = [
    {
        'id': '155978aa-8517-4eeb-9a3a-cb245c403970',
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus': [
            {
                'id': 'b0305dd7-04db-4bf7-adb6-a2fc217181be',
                'title': 'My submenu 1',
                'description': 'My submenu description 1',
                'dishes': [
                    {
                        'id': '3116d4ec-5aba-4649-8ff2-d71af25f7520',
                        'title': 'My dish 1',
                        'description': 'My dish description 1',
                        'price': '12.50'
                    }
                ]
            }
        ]
    }
]


@pytest.fixture
async def get_menu():
    return menu


@pytest.fixture
async def get_updated_menu():
    return menu_updated


@pytest.fixture
async def get_submenu():
    return submenu


@pytest.fixture
async def get_updated_submenu():
    return submenu_updated


@pytest.fixture
async def get_dish_1():
    return dish_1


@pytest.fixture
async def get_dish_2():
    return dish_2


@pytest.fixture
async def get_updated_dish():
    return dish_updated


@pytest.fixture
async def get_viewall():
    return viewall


@pytest.fixture
async def get_menuid_for_submenu_test(ac: AsyncClient, get_submenu):
    response = await ac.post('/api/v1/menus/',
                             json=get_submenu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_menuid(ac: AsyncClient, get_menu):
    response = await ac.post('/api/v1/menus/',
                             json=get_menu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_submenuid(ac: AsyncClient, get_menuid, get_submenu):
    test_menu_id = get_menuid
    response = await ac.post(f'/api/v1/menus/{test_menu_id}/submenus/',
                             json=get_submenu)
    result = response.json()
    test_submenu_id = result['id']
    return test_menu_id, test_submenu_id


@pytest.fixture
async def get_data_for_viewall_test(ac: AsyncClient, get_submenuid, get_dish_1):
    test_menu_id, test_submenu_id = get_submenuid
    response = await ac.post(f'/api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}/dishes/',
                             json=get_dish_1)
    result = response.json()
    test_dish_id = result['id']
    return test_menu_id, test_submenu_id, test_dish_id


@pytest.fixture
async def get_expected_viewall(get_data_for_viewall_test, get_viewall):
    test_menu_id, test_submenu_id, test_dish_id = get_data_for_viewall_test
    expected_result = get_viewall
    for menu in expected_result:
        menu['id'] = test_menu_id
        for submenu in menu['submenus']:
            submenu['id'] = test_submenu_id
            for dish in submenu['dishes']:
                dish['id'] = test_dish_id

    return expected_result
