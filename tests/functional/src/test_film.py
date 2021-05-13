import pytest


@pytest.mark.asyncio
async def test_get_all_films(prepare_es_film, make_get_request, get_all_data_elastic, redis_client):
    """Вывести все фильмы"""

    # получаем все фильмы из elasticsearch
    all_films = await get_all_data_elastic('movies')

    response = await make_get_request('/film', {'size': 1000, 'page': 1})

    assert response.status == 200

    assert len(response.body) == len(all_films)

    # очищаем кэш
    # await redis_client.flushdb()
    await redis_client.delete(str(response.url))


@pytest.mark.asyncio
async def test_search_detailed(prepare_es_film, make_get_request, redis_client):
    """Поиск конкретного фильма"""

    # Выполнение запроса
    response = await make_get_request('/film', {'query': 'abracadabra'})
    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 1

    assert response.body == prepare_es_film

    await redis_client.delete(str(response.url))


@pytest.mark.asyncio
async def test_get_by_id(prepare_es_film, make_get_request, redis_client):
    """Тест проверяет работу получения по id в эндпоинте film"""

    response = await make_get_request('/film/3a5f9a83-4b74-48be-a44e-a6c8beee9460')

    # Проверка результата
    assert response.status == 200

    assert response.body == prepare_es_film[0]

    await redis_client.delete(str(response.url))


@pytest.mark.asyncio
async def test_validator(make_get_request, redis_client):
    """Тест корректной валидации форм"""

    response = await make_get_request('/film')
    assert response.status == 200, 'empty parametr validator, status must be 200'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film/wrong-uuid')
    assert response.status == 422, 'wrong uuid validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'genre': 'wrong-uuid'})
    assert response.status == 422, 'wrong genre uuid validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'page': 101})
    assert response.status == 422, 'too large page validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'page': 0})
    assert response.status == 422, 'too small page validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'size': 2001})
    assert response.status == 422, 'too large size validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'size': 0})
    assert response.status == 422, 'too small size validator, status must be 422'
    await redis_client.delete(str(response.url))

    response = await make_get_request('/film', {'query': 'MovieNonExists'})
    assert response.status == 404, 'search non-existent movie validator, status must be 404'
    await redis_client.delete(str(response.url))

    # TODO тут должна быть ещё проверка кэша
