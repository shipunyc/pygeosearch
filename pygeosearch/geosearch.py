"""
The client for doing geo search.
"""

import geohash
import math
import redis
import thread

import pygeosearch.geohashsearch as geohashsearch
import pygeosearch.rw_lock as rw_lock
import pygeosearch.shared_redis as shared_redis


PREFIX_K2L = 'pgsk2l'  # from key to location
PREFIX_L2K = 'pgsl2k'  # from location to key


# Cell dimensions at the equator (in meters).
#
# The table below shows the metric dimensions for cells covered by various
# string lengths of geohash. Cell dimensions vary with latitude and so the
# table is for the worst-case scenario at the equator.
#
# Source: http://bit.ly/1tYJlIq
GEOHASH_CELL_SIZE = {
  1: (5009400, 4992600),
  2: (1252300, 624100),
  3: (156500, 156000),
  4: (39100, 19500),
  5: (4900, 4900),
  6: (1200, 609.4),
  7: (152.9, 152.4),
  8: (38.2, 19),
  9: (4.8, 4.8),
  10: (1.2, 0.595),
  11: (0.149, 0.149),
  12: (0.037, 0.019)
}


class GeoSearch(object):
  """ The client for doing geo search. """

  NUM_CELLS_IN_CIRCLE = 100
  # We use reader-writer lock to make this class thread-safe.
  _rw_lock = rw_lock.RWLock()

  def __init__(self, r=None, min_precision=4, max_precision=9):
    """Intializes a geo search client.
    Args:
      - `r`: redis.StrictRedis, the redis client.
      - `min_precision`: int, the minimum precision of a geo cell.
      - `max_precision`: int, the maximum precision of a geo cell.
    """
    if r:
      self._r = r
    else:
      # It's ok to share redis because it's thread-safe for our case.
      self._r = shared_redis.get_shared_redis()
    self._min_p = min_precision
    self._max_p = max_precision

  def put(self, lat, lon, key):
    """Adds or updates one key with its related latitude and longitude.
    Args:
      - `lat`: float, latitude
      - `lon`: float, longitude
      - `key`: str, the key to add to Redis.
    """
    GeoSearch._rw_lock.writer_acquire()
    try:
      new_cells = set([geohash.encode(lat, lon, precision=p)
                       for p in range(self._min_p, self._max_p + 1)])
      key_k2l = '%s:%s' % (PREFIX_K2L, key)
      non_existing_cells = set([])
      if self._r.exists(key_k2l):
        old_cells = set(self._r.smembers(key_k2l))
        non_existing_cells = old_cells - new_cells
        new_cells = new_cells - old_cells
      # Remove non-existing ones.
      for one_cell in non_existing_cells:
        self._r.srem(key_k2l, one_cell)
        self._r.srem('%s:%s' % (PREFIX_L2K, one_cell), key)
      # Add new ones.
      for one_cell in new_cells:
        self._r.sadd(key_k2l, one_cell)
        self._r.sadd('%s:%s' % (PREFIX_L2K, one_cell), key)
    finally:
      GeoSearch._rw_lock.writer_release()

  def rem(self, key):
    """Removes a key.
    Args:
      - `key`: str, the key to remove from Redis
    """
    GeoSearch._rw_lock.writer_acquire()
    try:
      key_k2l = '%s:%s' % (PREFIX_K2L, key)
      if not self._r.exists(key_k2l):
        return  # Ignore the key if it doesn't exist.
      old_cells = set(self._r.smembers(key_k2l))
      for one_cell in old_cells:
        self._r.srem(key_k2l, one_cell)
        self._r.srem('%s:%s' % (PREFIX_L2K, one_cell), key)
    finally:
      GeoSearch._rw_lock.writer_release()

  @staticmethod
  def _estimate_best_precision(radius):
    """Estimate the best precision for the given radius.
    Args:
      radius: float

    Returns:
      int, the best precision.
    """
    # Ideally, we want to devide the circle into GeoSearch.NUM_CELLS_IN_CIRCLE
    # pieces.
    desired_size = radius * 2 / math.sqrt(GeoSearch.NUM_CELLS_IN_CIRCLE)
    for i in range(1, 13):
      if max(GEOHASH_CELL_SIZE[i]) < desired_size:
        return i
    raise ValueError('The radius %s is too small.' % radius)

  def search_in_distance(self, lat, lon, distance, limit=1000):
    """Gets keys within a distance of (lat, lon).
    Args:
      lat: float, the latitude of the location.
      lon: float, the longitude of the location.
      distance: float, the distance.
      limit: int, the limit on the number of results to return.

    Returns:
      list, the list of keys.
    """
    # TODO: Return an iterable of the keys instead of returning a list.
    best_p = GeoSearch._estimate_best_precision(distance)
    if best_p < self._min_p or best_p > self._max_p:
      raise ValueError('The best precision for this radius %f is %d, ' +
                       'but you have min precision %d, ' +
                       'and max precision %d',
                       radius, best_p, self._min_p, self._max_p)
    # Find the cells inside the circle.
    cells = geohashsearch.get_cells_in_circle(lat, lon, distance, best_p)
    results = []
    GeoSearch._rw_lock.reader_acquire()

    try:
      for cell in cells:
        redis_key = '%s:%s' % (PREFIX_L2K, cell)
        if self._r.exists(redis_key):
          results.extend(list(self._r.smembers('%s:%s' % (PREFIX_L2K, cell))))
        if len(results) >= limit:
          break
    finally:
      GeoSearch._rw_lock.reader_release()

    return results[:limit]

  # TODO: Implement other kinds of search methods.
