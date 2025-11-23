import redis
import json

# Setup koneksi Redis (pastikan Redis jalan di localhost:6379)
cache = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cache(key: str):
    data = cache.get(key)
    return json.loads(data) if data else None

def set_cache(key: str, value: dict, expire: int = 3600):
    cache.set(key, json.dumps(value), ex=expire)

def clear_cache(key: str):
    cache.delete(key)

def clear_all_cache():
    cache.flushdb()
