from datetime import timedelta
from typing import Any, Type

from redis.client import Redis
from redis.cluster import RedisCluster
from redis.exceptions import RedisError

from modules.adapter.infrastructure.message.broker.interface import Cache
from modules.adapter.infrastructure.fastapi.config import Config, fastapi_config
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class RedisClient(Cache):
    def __init__(self, app_config: Config):
        self._client: Type[Redis] | RedisCluster | None = Redis
        self._keys: Any = None
        self._copied_keys: list = list()
        self._redis_url: str = app_config.REDIS_URL
        self._cluster_nodes: list = [
            app_config.REDIS_NODE_HOST_1,
            app_config.REDIS_NODE_HOST_2,
        ]

    def get_cluster_nodes(self):
        for node_host in self._cluster_nodes:
            node = dict()
            node["host"] = node_host
            node["port"] = 6379
            self._cluster_nodes.append(node)
        return self._cluster_nodes

    def connect(self):
        if self._cluster_nodes[0] is not None and self._cluster_nodes[1] is not None:
            startup_nodes = self.get_cluster_nodes()
            self._client: RedisCluster = RedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=False,
                skip_full_coverage_check=True,
            )
            logger.info("Redis Cluster is connected")
        else:
            self._client: Type[Redis] = self._client.from_url(self._redis_url)
            logger.info("Redis is connected")

    def disconnect(self) -> None:
        self._client.connection_pool.disconnect()
        logger.info("Redis is disconnected")

    def scan(self, pattern: str) -> None:
        self._keys = self._client.scan_iter(match=pattern)

    def get_after_scan(self) -> dict | None:
        try:
            key = next(self._keys)
            value = self._client.get(key)
            self._copied_keys.append(key)
            return {"key": key, "value": value}
        except StopIteration as e:
            return None

    def set(
        self, key: Any, value: Any, ex: int | timedelta | None = None
    ) -> bool | None:
        return self._client.set(name=key, value=value, ex=ex)

    def clear_cache(self) -> None:
        for key in self._copied_keys:
            self._client.delete(key)
        self._keys = None
        self._copied_keys = list()

    def get_by_key(self, key: str) -> str:
        return self._client.get(name=key)

    def flushall(self) -> None:
        self._client.flushall()

    def is_available(self) -> bool:
        try:
            self._client.ping()
        except RedisError:
            logger.error(f"[RedisClient][is_available] ping error")
            return False
        return True

    def sismember(self, set_name: str, value: str) -> bool:
        return self._client.sismember(name=set_name, value=value)

    def smembers(self, set_name: str) -> set[Any]:
        return self._client.smembers(name=set_name)


redis: RedisClient = RedisClient(fastapi_config)
