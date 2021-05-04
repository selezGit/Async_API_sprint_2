import abc
import json
from typing import Any, Optional
import backoff


class BaseService:  # 5 минут
    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs) -> Any:
        """Получить объект по uuid"""
        pass

    @abc.abstractmethod
    async def get_by_param(self, *args, **kwargs) -> Any:
        """Получить объекты по параметрам"""
        pass
