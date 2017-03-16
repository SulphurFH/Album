import redis

class RedisHelper(object):
    def __init__(self,host,port):
        self.__redis = redis.StrictRedis(host=host,port=port)

    def set(self,key,value):
        self.__redis.set(key,value)

    def get(self,key):
        return self.__redis.get(key)