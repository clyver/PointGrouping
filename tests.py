from point_grouping import distributed_indices, hash
import random
#import pdb; pdb.set_trace()

num_points = random.randint(0, 101)
num_groups = random.randint(0, num_points)
assert len(distributed_indices(num_points, num_groups)) == num_groups

point = {"lat": 40.577319, "lon": -74.010944, "id": "brooklyn"}
hashed_point = {'lat': 40.577319, 'lon': -74.010944, 'geohash': 'dr5qgffuh082', 'id': 'brooklyn'}
assert hash(point.get('lat'), point.get('lon'), point.get('id')) == hashed_point



