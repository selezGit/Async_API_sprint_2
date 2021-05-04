import logging
from functools import lru_cache
from typing import List, Optional, Dict

import backoff
from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends
from models.person import Person

from services.base import BaseService
from cache.base import BaseCache
from cache.redis_cache import RedisCache
from storage.person import PersonElasticStorage, PersonBaseStorage


class PersonBaseService(BaseService):
    async def get_by_id(self, url: str, id: str) -> Optional[Dict]:
        pass

    async def get_by_param(
        self, url: str, page: int, size: int, q: str = None
    ) -> List[Optional[Dict]]:
        pass


class PersonService(BaseService):
    def __init__(self, cache: BaseCache, storage: PersonBaseStorage):
        self.cache = cache
        self.storage = storage

    async def get_by_id(
        self,
        url: str,
        id: str,
    ) -> Optional[Dict]:
        """Получить объект по uuid"""
        data = await self.cache.check_cache(url)
        if not data:
            data = await self.storage.get(id=id)
            if data:
                await self.cache.load_cache(url, data)

        return data

    async def get_by_param(
        self, url: str, page: int, size: int, q: str = None
    ) -> Optional[List[Dict]]:
        """Найти объект(ы) по ключевому слову"""
        data = await self.cache.check_cache(url)
        if not data:
            data = await self.storage.get_multi(page=page, size=size, q=q)
            if data:
                await self.cache.load_cache(url, data)

        return data


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    cache = RedisCache(redis)
    storage = PersonElasticStorage(elastic)
    return PersonService(cache, storage)
