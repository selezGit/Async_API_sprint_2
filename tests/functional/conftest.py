import asyncio

import aiohttp
import aioredis_cluster
import pytest
from elasticsearch import AsyncElasticsearch, helpers, exceptions


from settings import SETTINGS, logger
from testdata.models import HTTPResponse
from utils.bulk_helper import delete_doc, generate_doc
from utils.wait_for_es import wait_es
from typing import Any

SERVICE_URL = 'http://127.0.0.1:8000'


@pytest.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(hosts=[SETTINGS.es_host, ])
    yield client
    await client.close()


@pytest.fixture(scope='function')
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()


@pytest.fixture(scope='function')
async def redis_client():
    client = await aioredis_cluster.create_redis_cluster([SETTINGS.redis_host])
    yield client
    await client.close()


@pytest.fixture
async def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        # в боевых системах старайтесь так не делать!
        url = SETTINGS.back_host + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest.fixture(scope='function')
async def prepare_es_film(es_client):
    index = 'movies'
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
    await wait_es()

    await helpers.async_bulk(es_client, generate_doc(data, index))
    logger.info('data is uploaded')
    # ждём секунду, что бы данные успели загрузиться в elastic
    await asyncio.sleep(1)

    yield data

    await helpers.async_bulk(es_client, delete_doc(data, index))
    logger.info('data is deleted')


@pytest.fixture
async def get_all_data_elastic(es_client):
    async def inner(index: str) -> Any:
        query = {
            "query": {
                "match_all": {}
            }
        }

        try:
            doc = await es_client.search(index=index, body=query, size=10000)
        except exceptions.NotFoundError:
            return []

        if not doc:
            return []
        result = doc["hits"]["hits"]

        if not result:
            return []

        return [data["_source"] for data in result]
    return inner
