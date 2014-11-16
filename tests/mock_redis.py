"""
Mocks the redis client.
"""

import redis

class MockRedis(object):

  def __init__(self):
    self._data = {}

  def sadd(self, key, value):
    """Mocks the sadd method.
    :Parameters:
      - `key`: str, the redis key.
      - `value`: str, the value to add.
    """
    if not self._data.get(key):
      self._data[key] = set([])
    self._data[key].add(value)

  def srem(self, key, value):
    """Mocks the srem method.
    :Parameters:
      - `key`: str, the redis key.
      - `value`: str, the value to remove.
    """
    if self._data.get(key):
      self._data[key].remove(value)

  def smembers(self, key):
    """Mocks the smembers method.
    :Parameters:
      - `key`: str, the redis key.

    :Returns:
      set, the set of values at the key.
    """
    return self._data[key]

  def exists(self, key):
    """Mocks the exists method.
    :Parameters:
      - `key`: str, the redis key.

    :Returns:
      boolean
    """
    return key in self._data
