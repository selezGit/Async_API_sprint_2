import pytest
import repackage

repackage.up()

from conftest import make_get_request

@pytest.mark.asyncio
async def test_search_detailed(es_client):
    # Заполнение данных для теста
    await es_client.bulk(...)

    # Выполнение запроса
    response = await make_get_request('/search', {'search': 'Star Wars'})
    # Проверка результата
    assert response.status == 200
    assert len(response.body) == 1

    assert response.body == 200