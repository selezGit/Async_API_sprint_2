import pytest

@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):
    # Заполнение данных для теста
    # await es_client.bulk(...)
    print('here')
    # Выполнение запроса
    response = await make_get_request('/search', {'search': 'Star Wars'})
    print(response)
    # Проверка результата
    assert response.status == 200
    assert len(response.body) == 1

    assert response.body == 200