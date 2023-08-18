# mypy: disable-error-code="name-defined"
from httpx import AsyncClient

prefix = '/api/v1/viewall'


async def test_reading_all_data(ac: AsyncClient, get_expected_viewall: dict) -> None:
    response = await ac.get(f'{prefix}/')
    assert response.status_code == 200
    assert response.json() == get_expected_viewall
