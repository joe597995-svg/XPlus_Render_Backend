# utils/redis_client.py
import redis

def get_redis():
    try:
        return redis.Redis(host="redis", port=6379, db=0)
    except:
        return None
