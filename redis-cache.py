import redis
import json

redis_host = "localhost"
redis_port = 6379
redis_password = ""


def get_redis():
    try:
        return redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
    except Exception as e:
        print(e)


def cache_user_data(uuid, data):
    get_redis().set(uuid, json.dumps(data))


def get_user_cache(uuid):
    return json.loads(get_redis().get(uuid)).decode('utf-8')