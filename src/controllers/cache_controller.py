from models.redis_model import RedisModel


class CacheController(RedisModel):
    def __init__(self):
        super(CacheController, self).__init__()
