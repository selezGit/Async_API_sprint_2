from abc import abstractmethod, ABC


class BaseView(ABC):
    @classmethod
    @abstractmethod
    async def get_all(cls):
        """Возвращает инф-ию по всем объектам с возможностью пагинации"""
        pass

    @classmethod
    @abstractmethod
    async def get_details(cls):
        """Возвращает информацию по одному объекту"""
        pass
