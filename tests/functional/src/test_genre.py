import pytest


@pytest.mark.asyncio
async def test_genre_all_valid_data(prepare_es_genre, make_get_request):
    # Выполнение запроса
    response = await make_get_request('/genre/', {'page': 1, 'size': 20})
    # Проверка результата
    assert response.status == 200
    assert len(response.body) >= 1


@pytest.mark.asyncio
async def test_genre_all_not_valid_params(prepare_es_genre, make_get_request):
    # Выполнение запроса
    response = await make_get_request('/genre/', {'page': -1, 'size': 1})
    assert response.status == 422

    response = await make_get_request('/genre/', {'page': 1, 'size': 0})
    assert response.status == 422


@pytest.mark.asyncio
async def test_genre_detail_valid_data(prepare_es_genre, make_get_request):
    # Выполнение запроса
    response = await make_get_request('/genre/e91db2b1-d967-4785-bec9-1eade1d56243')
    # Проверка результата
    assert response.status == 200
    assert response.body == prepare_es_genre[0]

    # запрос не существующего жанра
    response = await make_get_request('/genre/6aea47a2-7db0-4bf6-a05a-31ea35eb3cde')
    assert response.status == 404


@pytest.mark.asyncio
async def test_genre_detail_not_valid_data(prepare_es_genre, make_get_request):
    # Выполнение запроса
    response = await make_get_request('/genre/1-not-valid-uuid')
    # Проверка результата
    assert response.status == 422

    response = await make_get_request('/genre/1')

    assert response.status == 422
