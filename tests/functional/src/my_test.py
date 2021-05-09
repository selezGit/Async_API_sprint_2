import pytest
import repackage

repackage.up()

from conftest import make_get_request


@pytest.mark.asyncio
async def test_search_detailed():
    # Заполнение данных для теста
    # await es_client.bulk(...)

    # Выполнение запроса
    assert 1 == False
