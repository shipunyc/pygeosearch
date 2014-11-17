"""
Creates a shared instance of Redis.
"""

import redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


shared_redis_instance = None


def get_shared_redis():
  """Gets a shared Redis client.
  Returns:
    redis.StrictRedis
  """
  global shared_redis_instance
  if not shared_redis_instance:
    shared_redis_instance = redis.StrictRedis(host=REDIS_HOST,
                                              port=REDIS_PORT,
                                              db=REDIS_DB)
  return shared_redis_instance
