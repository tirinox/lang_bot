import redis.asyncio


class DB:
    def __init__(self, env_dict):
        self.redis = redis.asyncio.Redis(
            host=env_dict['REDIS_HOST'],
            port=env_dict['REDIS_PORT'],
            db=env_dict['REDIS_DB_INDEX'],
            password=env_dict['REDIS_PASSWORD'],
        )
