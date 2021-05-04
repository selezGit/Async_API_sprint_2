
from abc import abstractclassmethod, ABC


class BaseView(ABC):

    @abstractclassmethod
    async def get_all(self):
        """Возвращает инф-ию по всем объектам с возможностью пагинации"""
        pass

    @abstractclassmethod
    async def get_details(self):
        """Возвращает информацию по одному объекту"""
        pass
