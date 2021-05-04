import logging
from functools import lru_cache
from typing import Dict, List, Optional
import abc
import backoff
from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film

from services.base import BaseService
from cache.base import BaseCache
from cache.redis_cache import RedisCache

from storage.film import FilmBaseStorage, FilmElasticStorage


class FilmBaseService(BaseService):
    @abc.abstractmethod
    async def get_by_id(self, url: str, id: str) -> Optional[Dict]:
        pass

    @abc.abstractmethod
    async def get_by_param(
        self,
        url: str,
        order: str,
        page: int,
        size: int,
        genre: str = None,
        query: str = None,
    ) -> List[Optional[Dict]]:
        pass

    @abc.abstractmethod
    async def get_by_list_id(self, url: str, film_ids: List[str]) -> Optional[Dict]:
        pass


class FilmService(FilmBaseService):
    def __init__(self, cache: BaseCache, storage: FilmBaseStorage):
        self.cache = cache
        self.storage = storage

    async def get_by_id(self, url: str, id: str) -> Optional[Dict]:
        """Функция получения фильма по id"""
        film = await self.cache.check_cache(url)
        if not film:
            film = await self.storage.get(id=id)
            if not film:
                return None

            await self.cache.load_cache(url, film)

        return film

    async def get_by_list_id(
        self,
        url: str,
        film_ids: List[str],
        page: int,
        size: int,
    ) -> List[Optional[Dict]]:
        """Функция получения фильмов по id"""

        data = await self.cache.check_cache(url)
        if not data:
            data = await self.storage.get_with_list_id(
                film_ids=film_ids, page=page, size=size
            )
            if data:
                await self.cache.load_cache(url, data)
        return data

    async def get_by_param(
        self,
        url: str,
        order: str,
        page: int,
        size: int,
        genre: str = None,
        query: str = None,
    ) -> List[Optional[Film]]:
        """Функция получения всех фильмов с параметрами сортфировки и фильтрации"""
        films = await self.cache.check_cache(url)
        if not films:

            films = await self.storage.get_multi(
                page=page, size=size, order=order, genre=genre, q=query
            )
            if films:
                await self.cache.load_cache(url, films)
        return films


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    cache = RedisCache(redis=redis)
    storage = FilmElasticStorage(elastic)
    return FilmService(cache, storage)
