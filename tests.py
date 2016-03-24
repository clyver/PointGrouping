from point_grouping import group
import json

grouped_points = [[u'brooklyn2',
                   u'brooklyn1',
                   u'brooklyn3',
                   u'manhattan1',
                   u'manhattan2',
                   u'manhattan3',
                   u'manhattan4'],
                  [u'bronx1',
                   u'bronx2',
                   u'bronx3',
                   u'london1',
                   u'london2',
                   u'cairo2',
                   u'cairo1'],
                  [u'athens2',
                   u'athens1',
                   u'paris2',
                   u'paris1',
                   u'moscow2',
                   u'moscow1']]

non_grouped_points = [[u'brooklyn2',
                       u'brooklyn1',
                       u'brooklyn3',
                       u'manhattan1',
                       u'manhattan2',
                       u'manhattan3',
                       u'manhattan4',
                       u'bronx1',
                       u'bronx2',
                       u'bronx3',
                       u'london1',
                       u'london2',
                       u'cairo2',
                       u'cairo1',
                       u'athens2',
                       u'athens1',
                       u'paris2',
                       u'paris1',
                       u'moscow2',
                       u'moscow1']]

# group() Tests
json_data = open('./initialExperiments/sample_points.json').read()
points = json.loads(json_data)
assert group(points, 3) == grouped_points
assert group(points, 0) == non_grouped_points
