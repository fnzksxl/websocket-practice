import redis
from threading import Lock

class RedisConnectionPool:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, host='localhost', port=6379, db=0, max_connections=10):
        if not hasattr(self, '_pool'):
            self._pool = redis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                max_connections=max_connections
            )
        
    def get_redis_client(self):
        return redis.Redis(connection_pool=self._pool)
