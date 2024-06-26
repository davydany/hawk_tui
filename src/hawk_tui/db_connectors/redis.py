import redis
from typing import List, Union, Dict, Any
from hawk_tui.db_connectors.base import BaseConnection

class RedisConnection(BaseConnection):

    def connect(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            db=self.database,
            decode_responses=True
        )

    def is_connected(self) -> bool:
        try:
            self.connection.ping()
            return True
        except redis.ConnectionError:
            return False

    def close(self):
        self.connection.close()

    def list_databases(self) -> List[int]:
        return list(range(16))  # Redis typically has 16 databases by default

    def set(self, key: str, value: str) -> bool:
        return self.connection.set(key, value)

    def get(self, key: str) -> Union[str, None]:
        return self.connection.get(key)

    def incr(self, key: str, amount: int = 1) -> int:
        return self.connection.incr(key, amount)

    def decr(self, key: str, amount: int = 1) -> int:
        return self.connection.decr(key, amount)

    def mget(self, keys: List[str]) -> List[Union[str, None]]:
        return self.connection.mget(keys)

    def expire(self, key: str, seconds: int) -> bool:
        return self.connection.expire(key, seconds)

    def ttl(self, key: str) -> int:
        return self.connection.ttl(key)

    def persist(self, key: str) -> bool:
        return self.connection.persist(key)

    def scan(self, cursor: int = 0, match: str = None, count: int = None) -> tuple:
        return self.connection.scan(cursor, match, count)

    def delete(self, *keys: str) -> int:
        return self.connection.delete(*keys)

    def info(self) -> Dict[str, Any]:
        return self.connection.info()

    def list_keys(self, pattern: str = "*") -> List[str]:
        keys = []
        cursor = 0
        while True:
            cursor, batch = self.scan(cursor, match=pattern)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys