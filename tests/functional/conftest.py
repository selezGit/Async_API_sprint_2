import aiohttp
import aioredis_cluster
import pytest
from elasticsearch import AsyncElasticsearch

from testdata.models import HTTPResponse

from settings import TestSettings

SERVICE_URL = 'http://127.0.0.1:8000'

SETTINGS = TestSettings()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=[SETTINGS.es_host,])
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
        url = SETTINGS.back_host + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner