import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from menu_app import models
from menu_app.database import get_db, get_url
from menu_app.main import app
from menu_app.tests.data import (
    dish_1_test,
    dish_2_test,
    dish_updated_test,
    menu_test,
    menu_updated_test,
    submenu_test,
    submenu_updated_test,
    viewall_test,
)

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


@pytest.fixture
async def get_menu():
    return menu_test


@pytest.fixture
async def get_updated_menu():
    return menu_updated_test


@pytest.fixture
async def get_submenu():
    return submenu_test


@pytest.fixture
async def get_updated_submenu():
    return submenu_updated_test


@pytest.fixture
async def get_dish_1():
    return dish_1_test


@pytest.fixture
async def get_dish_2():
    return dish_2_test


@pytest.fixture
async def get_updated_dish():
    return dish_updated_test


@pytest.fixture
async def get_viewall():
    return viewall_test


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
