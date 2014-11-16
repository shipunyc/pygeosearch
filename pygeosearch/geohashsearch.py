"""
Functions for performing geosearch using geohash cells.
"""

import geohash
import math


def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two point on the earth.

    Args:
      - `lat1`: float
      - `lon1`: float
      - `lat2`: float
      - `lon2`: float

    Returns:
      the distance in meters.
    """
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat/2)**2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))

    # 6367000 m is the radius of the Earth
    distance = 6367000 * c
    return distance


def get_cells_in_circle(lat, lon, radius, precision):
  """Gets all geohash cells inside a circle, sorted approximately by distance.

  Args:
    lat: float, the latitude of the circle center.
    lon: float, the longitude of the circle center.
    radius: float, the radius of the circle in meters.
    precision: int, the precision of the geohash.

  Returns:
    list, the list of geohash cells.
  """
  # Get all cells that are in the circle (with the max_resolution).
  # Start from the center cell.
  cur_set = set([geohash.encode(lat, lon, precision)])
  all_set = set(cur_set)
  result = list(cur_set)
  while cur_set:
    # Gradually extend the found cells (all_set) layer by layer.
    new_set = set([])
    for cell in cur_set:
      for one_neighbor in geohash.neighbors(cell):
        if one_neighbor in all_set:
          continue
        (nb_lat, nb_lon) = geohash.decode(one_neighbor)
        if distance(nb_lat, nb_lon, lat, lon) < radius:
          new_set.add(one_neighbor)
    all_set.update(new_set)
    result.extend(list(new_set))
    cur_set = new_set

  return result
