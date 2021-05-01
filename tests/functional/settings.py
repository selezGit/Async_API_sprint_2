from pydantic import BaseSettings, Field


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: list = Field(["redis://redis-node-0",
                              "redis://redis-node-1",
                              "redis://redis-node-2",
                              "redis://redis-node-3",
                              "redis://redis-node-4",
                              "redis://redis-node-5",
                              ], env='REDIS_HOST')
