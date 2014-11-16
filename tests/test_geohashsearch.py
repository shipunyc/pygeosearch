"""
Unit-test for the geohashsearch module
"""

import geohash
import unittest

import pygeosearch.geohashsearch as geohashsearch


class TestAllFunctions(unittest.TestCase):
  """ Test functions in geohashsearch. """

  def test_get_cells_in_circle(self):
    """Test geohashsearch.get_cells_in_circle
    """
    lat = 42.6
    lon = -5.7
    distance = 100
    precision = 9
    cells = geohashsearch.get_cells_in_circle(lat, lon, 100, precision)
    self.assertTrue(len(cells) > 0)
    # The first cell should be the center.
    self.assertEquals(geohash.encode(lat, lon, precision), cells[0])
    # And every cell is in the circle.
    for cell in cells:
      (c_lat, c_lon) = geohash.decode(cell)
      self.assertTrue(geohashsearch.distance(c_lat, c_lon, lat, lon) < distance)
