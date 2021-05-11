import pytest

@pytest.mark.asyncio
async def test_search_detailed(prepare_es_film, make_get_request):
    """Поиск конкретного фильма"""

    # Выполнение запроса
    response = await make_get_request('/film', {'query': 'abracadabra'})
    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 1

    assert response.body == prepare_es_film

@pytest.mark.asyncio
async def test_get_by_id(prepare_es_film, make_get_request):
    """Тест проверяет работу получения по id в эндпоинте film"""

    response = await make_get_request('/film/3a5f9a83-4b74-48be-a44e-a6c8beee9460')

    # Проверка результата
    assert response.status == 200

    assert response.body == prepare_es_film[0]

@pytest.mark.asyncio
async def test_get_all_films(make_get_request, get_all_data_elastic):
    """Вывести все фильмы"""

    #получаем все фильмы из elasticsearch    
    all_films= await get_all_data_elastic('movies')

    response = await make_get_request('/film', {'size': 1000, 'page': 1})

    assert response.status == 200

    assert len(response.body) == len(all_films)