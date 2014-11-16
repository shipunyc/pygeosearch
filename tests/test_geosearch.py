"""
Unit-test for the geosearch module
"""

import unittest

import geosearch as geosearch
import tests.mock_redis as mock_redis


class TestAllFunctions(unittest.TestCase):
  """ Test functions in geosearch. """

  def setUp(self):
    """ Sets up. """
    self._mock_redis = mock_redis.MockRedis()

  def test_search_in_distance(self):
    """Test geosearch.search_in_distance
    """
    client = geosearch.GeoSearch(self._mock_redis,
                                 min_precision=1,
                                 max_precision=9)

    # Add a few keys.
    lat0 = 42.6
    lon0 = -5.7
    client.put(lat0, lon0, 'key1')
    client.put(lat0, lon0, 'key2')
    client.put(lat0, lon0, 'key3')
    lat1 = 42.61  # Close enough
    lon1 = -5.72
    client.put(lat1, lon1, 'key1')
    client.put(lat1, lon1, 'key4')
    client.put(lat1, lon1, 'key5')
    lat2 = 45.6  # Far from (lat0, lon0) and (lat1, lon1)
    lon2 = -15.7
    client.put(lat0, lon2, 'key2')
    client.put(lat0, lon2, 'key6')
    client.put(lat0, lon2, 'key7')

    keys = client.search_in_distance(lat0, lon0, 10000)  #10km
    # We will get key1, key3, key4, key5
    self.assertEqual(4, len(keys))
    self.assertTrue('key1' in keys)
    self.assertTrue('key3' in keys)
    self.assertTrue('key4' in keys)
    self.assertTrue('key5' in keys)

    keys = client.search_in_distance(lat0, lon0, 10000000)  #10000km
    # Now we have everyting
    self.assertEqual(7, len(keys))
    self.assertTrue('key2' in keys)
    self.assertTrue('key6' in keys)
    self.assertTrue('key7' in keys)
