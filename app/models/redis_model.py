import logging

import redis

from configs.redis_config import RedisConfig
from helpers.utils import get_environment


class RedisModel(object):
    def __init__(self):
        self.infra_env = get_environment()
        self.instance_config = RedisConfig().INSTANCE_CONFIG.get(self.infra_env, {})

    def get_connection(self):
        try:
            connection = redis.Redis(host=self.instance_config.get("host"),
                                     port=self.instance_config.get("port"),
                                     db=self.instance_config.get("db"),
                                     password=self.instance_config.get("password"),
                                     socket_timeout=self.instance_config.get("socket_timeout"),
                                     )
            return connection
        except Exception as err:
            logging.error(f'error from get_connection occurred due to {err}')
            raise

    def get(self, redis_key):
        try:
            redis_connection = self.get_connection()
            result = redis_connection.get(redis_key)
            return result
        except Exception as err:
            logging.error(f'error from get_query occurred due to {err}')
            raise

    def set(self, redis_key, value):
        try:
            redis_connection = self.get_connection()
            redis_connection.set(redis_key, value)
        except Exception as err:
            logging.error(f'error from set_query occurred due to {err}')
            raise

    def delete(self, redis_key):
        try:
            redis_connection = self.get_connection()
            redis_connection.delete(redis_key)
        except Exception as err:
            logging.error(f'error from delete_query occurred due to {err}')
            raise
