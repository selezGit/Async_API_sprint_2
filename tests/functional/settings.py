from pydantic import BaseSettings, Field
import logging
from typing import Any

logger = logging.getLogger('tests')
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)
logger.setLevel('DEBUG')


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class TestSettings(BaseSettings):
    back_host: str = Field('http://back:8000', env='FASTAPI_HOST')
    es_host: str = Field('elasticsearch:9200', env='ELASTIC_HOST')
    redis_host: str = Field('redis://redis-node-0', env='REDIS_HOST')


SETTINGS = TestSettings()