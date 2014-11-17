Py-GeoSearch
=========


### Introduction

Py-GeoSearch allows you to perform geo-spacial search using Redis as the only
in-memory data store. And this libary works with keys associated with geo-
locations, with which you can add / update / remove keys from the geo-space,
and efficiently query for keys.

Paired with other Redis data or relational database, Py-GeoSearch can assist
you implement advanced geo-spacial search algorithms.


### System Requirements

1. Redis [http://redis.io/download](http://redis.io/download)
2. python 2.7.x
3. python development headers (sudo apt-get install python-dev)


### Installation
```
pip install pygeosearch
```
or
```
python setup.py install
```


### Tests
Run unit tests with:
```
python setup.py test
```


### Example

```
import pygeosearch

client = pygeosearch.GeoSearch()

lat0 = 42.6
lon0 = -5.7
client.put(lat0, lon0, 'key1')

lat1 = 42.61  # Close enough
lon1 = -5.72
client.put(lat1, lon1, 'key1')
client.put(lat1, lon1, 'key2')
client.put(lat1, lon1, 'key3')

lat2 = 45.6  # Far from (lat0, lon0) and (lat1, lon1)
lon2 = -15.7
client.put(lat2, lon2, 'key3')  # updates 'key3' location.
client.put(lat2, lon2, 'key4')

keys = client.search_in_distance(lat0, lon0, 10000)  #10km
print keys
# You will get 'key1' and 'key2'

client.rem('key2')  # Removes 'key2'
keys = client.search_in_distance(lat0, lon0, 10000)  #10km
print keys
# You will get 'key1'
```
