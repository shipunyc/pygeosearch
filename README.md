Py-GeoSearch
=========


### System Requirements

1. Redis [http://redis.io/download](http://redis.io/download)
2. python 2.7.x
3. python development headers (sudo apt-get install python-dev)


### Installation
```
pip install pygeosearch
```
### Example

```
import geosearch

client = geosearch.GeoSearch()

lat0 = 42.6
lon0 = -5.7
client.put(lat0, lon0, 'key1')

lat1 = 42.61  # Close enough
lon1 = -5.72
client.put(lat1, lon1, 'key1')
client.put(lat1, lon1, 'key2')

lat2 = 45.6  # Far from (lat0, lon0) and (lat1, lon1)
lon2 = -15.7
client.put(lat0, lon2, 'key3')

keys = client.search_in_distance(lat0, lon0, 10000)  #10km
# You will get 'key1' and 'key2'
```
