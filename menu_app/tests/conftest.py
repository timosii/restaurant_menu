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


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest.fixture(scope='module')
async def clean_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


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
async def get_menuid_for_submenu_test(ac: AsyncClient, get_submenu):
    response = await ac.post('/api/v1/menus/',
                             json=get_submenu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_menuid_for_dish_test(ac: AsyncClient, get_menu):
    response = await ac.post('/api/v1/menus/',
                             json=get_menu)
    result = response.json()
    test_menu_id = result['id']
    return test_menu_id


@pytest.fixture
async def get_submenuid_for_dish_test(ac: AsyncClient, get_menuid_for_dish_test, get_submenu):
    test_menu_id = get_menuid_for_dish_test
    response = await ac.post(f'/api/v1/menus/{test_menu_id}/submenus/',
                             json=get_submenu)
    result = response.json()
    test_submenu_id = result['id']
    return test_menu_id, test_submenu_id
