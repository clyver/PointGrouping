import Geohash
from geopy.distance import vincenty
import json


json_data=open('sample_points.json').read()
points = json.loads(json_data).get('points')

geohash = "geohash"
lat = "lat"
lon = "lon"
id = "id"


def hash(point_lat, point_lon, point_id):
    """
    Create a geohash for the given coordinate
    :param point_lat: Float representing a latitude value
    :param point_lon: Float representing a longitude value
    :param point_id: String representing a unique identifier for this point
    :return: Dict containing the input parameters, plus the newly created geohash
    """
    return {geohash: Geohash.encode(lat, lon),
            lat: point_lat,
            lon: point_lon,
            id: point_id
            }

hashed_points = []
for point in points:
    lat = point.get(lat)
    lon = point.get(lon)
    pid = point.get(id)
    hashed_points.append(hash(lat, lon, pid))

print "Unsorted Hashes:"
for h in hashed_points:
    print h.get('id')

print ""
print "Hashes Sorted:"
sorted_hashes = sorted(hashed_points, key=lambda x: x.get('hash'))

for h in sorted_hashes:
    print h.get('id')
"""
len_hashes = len(sorted_hashes)
i = 0
while i < len_hashes - 1:
    a = (sorted_hashes[i].get('lat'), sorted_hashes[i].get('lon'))
    b = (sorted_hashes[i+1].get('lat'), sorted_hashes[i+1].get('lon'))

    print vincenty_dist(a, b)
    i += 1

"""



