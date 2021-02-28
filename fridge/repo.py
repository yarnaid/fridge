import typing
import models  # type: ignore
from datetime import datetime


class MemStorage(object):
    def __init__(self):
        self._items: typing.Dict[int, models.Item] = {}

    def get(self, id_: int) -> models.Item:
        return self._items[id_]

    def update(self, id_: int, item: models.Item) -> models.Item:
        self._items[id_] = item
        self._items[id_].updated_at = datetime.now()
        return self._items[id_]

    def delete(self, id_: int):
        del self._items[id_]

    def create(self, item: models.Item) -> int:
        if not self._items:
            id_ = 0
        else:
            id_ = max(self._items.keys()) + 1
        item.id = id_
        item.updated_at = datetime.now()
        item.stored_at = datetime.now()
        self._items[id_] = item
        return id_

    def get_all(self) -> typing.List[models.Item]:
        return list(self._items.values())
