class RedisConfig(object):
    INSTANCE_CONFIG = {'local': {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": None,
        "socket_timeout": None
    }, 'qa': {
        "host": "10.11.XX.XX",
        "port": 6379,
        "db": 0,
        "password": None,
        "socket_timeout": None
    }, 'prod': {
        "host": "10.11.XX.XX",
        "port": 6379,
        "db": 0,
        "password": None,
        "socket_timeout": None
    }}

