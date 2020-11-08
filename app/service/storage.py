import pickle
from typing import Any, Optional

from redis import Redis


class RedisInterface:

    serializer = pickle

    def __init__(self, redis: Redis, prefix: str, life_time: int):

        self._redis = redis
        self._prefix = prefix
        self._life_time = life_time

    def save(self, data: Any, sid: str) -> None:
        """
        Сохраняет данные в хранилище.
        Передаваемые данные должны быть сереализуемы в pickle.
        """

        pickled_data = self.serializer.dumps(data)

        self._redis.setex(
            name=self._prefix + sid, value=pickled_data,
            time=get_storage_time(self._life_time)
        )

    def get(self, sid: str) -> Optional[Any]:
        """Получает данные из хранилища."""

        data = self._redis.get(self._prefix + sid)

        if data is not None:
            data = self.serializer.loads(data)

        return data


class Storage:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.interface = self.init_app(app)

    @staticmethod
    def init_app(app):
        config = app.config.copy()

        config.setdefault('STORAGE_KEY_PREFIX', '__-__:')
        config.setdefault('STORAGE_LIFETIME', 60)

        storage_interface = RedisInterface(
            redis=config['STORAGE_REDIS'],
            prefix=config['STORAGE_KEY_PREFIX'],
            life_time=config['STORAGE_LIFETIME']
        )

        return storage_interface


def get_storage_time(minute: int) -> int:
    """Возбращает время хранения в секундах."""
    return 60 * minute