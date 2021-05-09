import pytest

@pytest.mark.asyncio
async def test_search_detailed(prepare_es_film, make_get_request):
    # data = 
    # Выполнение запроса
    response = await make_get_request('/film', {'query': 'abracadabra'})
    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 1

    assert response.body == prepare_es_film
