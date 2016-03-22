from point_grouping import distributed_indices, hash, find_anchors, nearest_neighbor, group
import random, json

# Some points we'll refer to
point1 = {"lat": 40.577319, "lon": -74.010944, "id": "brooklyn"}
point2 = {"lat": 40.714353, "lon": -74.013074, "id": "manhattan1"}
point3 = {"lat": 40.735091, "lon": -74.007109, "id": "manhattan2"}

grouped_points = {u'brooklyn2': [u'brooklyn2',
                        u'brooklyn1',
                        u'brooklyn3'],
                  u'cairo1': [u'london1',
                              u'london2',
                              u'cairo2',
                              u'cairo1',
                              u'athens2',
                              u'athens1',
                              u'paris2',
                              u'paris1',
                              u'moscow2',
                              u'moscow1'],
                  u'manhattan4': [u'manhattan1',
                                  u'manhattan2',
                                  u'manhattan3',
                                  u'manhattan4',
                                  u'bronx1',
                                  u'bronx2',
                                  u'bronx3']}

# distributed_indices() Tests
num_points = random.randint(0, 101)
num_groups = random.randint(0, num_points)
assert len(distributed_indices(num_points, num_groups)) == num_groups

# hash() Tests
hashed_point1 = {'lat': 40.577319, 'lon': -74.010944, 'geohash': 'dr5qgffuh082', 'id': 'brooklyn'}
assert hash(point1.get('lat'), point1.get('lon'), point1.get('id')) == hashed_point1


# find_anchors() Tests
indices = [(0, [5]), (4, [5]), (5, [5]), (8, [5, 10]), (20, [15])]
anchors = [5, 10, 15]
for index, anchor in indices:
    assert find_anchors(index, anchors) == anchor

# nearest_neighbor() Tests
assert nearest_neighbor(point2, point3, point1) == point3

# group() Tests
json_data = open('./initialExperiments/sample_points.json').read()
points = json.loads(json_data)
assert group(points, 3) == grouped_points
