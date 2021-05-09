import pytest
from elasticsearch import helpers
from datetime import datetime
from uuid import UUID


def generate_doc(docs):
    for doc in docs:
        yield {
            '_index': 'movies',
            '_id': doc['id'],
            '_source': doc
        }


@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):
    # Заполнение данных для теста
    data = [{'id': '3a5f9a83-4b74-48be-a44e-a6c8beee9460',
             'title': 'abracadabra',
             'description': '',
             'imdb_rating': 0,
             'creation_date': '1970-01-01T00:00:00',
             'restriction': 0,
             'directors': [],
             'actors': [],
            'writers': [],
             'genres': [],
             'file_path': ''}]
    await helpers.async_bulk(es_client, generate_doc(data))
    # Выполнение запроса
    response = await make_get_request('/film', {'query': 'abracadabra'})
    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 1

    assert response.body == data
