from redis import Redis


class RedisTools:
    __REDIS_CONNECT = Redis("172.28.0.2")

    @property
    def connection(self):
        return self.__REDIS_CONNECT


client = RedisTools()

session = client.connection
