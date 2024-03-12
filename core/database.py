import os

from dotenv import load_dotenv
from redis import Redis

load_dotenv()


class RedisTools:
    __CONNECTION = Redis(os.getenv("redis_url"))

    @property
    def connection(self):
        return self.__CONNECTION


client = RedisTools()


session = client.connection
