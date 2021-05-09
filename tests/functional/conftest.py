import aiohttp
import aioredis_cluster
import pytest
from elasticsearch import AsyncElasticsearch, helpers
from typing import List
from settings import TestSettings
from testdata.models import HTTPResponse
from utils.bulk_helper import generate_doc, delete_doc
import logging



SERVICE_URL = 'http://127.0.0.1:8000'

SETTINGS = TestSettings()

logger = logging.getLogger("TESTS")
logger.setLevel("DEBUG")


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=["localhost:9200"])
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    async with aiohttp.ClientSession(trust_env=False) as session:
        yield session
    await session.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis_cluster.create_redis_cluster(SETTINGS.redis_host)
    yield client
    await client.close()

@pytest.fixture
async def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        # в боевых системах старайтесь так не делать!
        url = SERVICE_URL + '/api/v1' + method
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

    await helpers.async_bulk(es_client, generate_doc(data, index))
    logger.info('data is uploaded')

    yield data

    await helpers.async_bulk(es_client, delete_doc(data, index))
    logger.info('data is deleted')

    