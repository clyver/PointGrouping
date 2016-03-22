import Geohash
from geopy.distance import vincenty
import json
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Some recurring strings we'll be referencing
geohash = "geohash"
lat = "lat"
lon = "lon"
id = "id"


def initialize():
    """
    Read in the necessary data.  This includes our lat/lon points and
    the number of desired groups.
    :return: A tuple containing the points and the specified number of groups
    """
    # Read in the points we'll be grouping
    try:
        json_data = open('./points.json').read()
        points = json.loads(json_data)
        num_points = len(points)
    except IOError:
        print "points.json file not found in the current directory!"
        sys.exit(1)
    except ValueError:
        print "Invalid JSON found in points.json!"
        sys.exit(1)

    # Determine the number of desired groups
    cli_input = sys.argv
    try:
        args_len = len(cli_input)
        if args_len != 2:
            raise TypeError("point_grouping.py takes exactly 1 argument, ({} given)!".format(args_len - 1))

        # Can generate a ValueError:
        num_groups = int(cli_input[1])

        if num_groups > num_points:
            raise TypeError("point_grouping.py must not have more groups ({}) than points ({})!".format(num_groups, num_points))
    except TypeError as e:
        print e
        sys.exit(1)
    except ValueError:
        print "point_groupoings.py expects a single INTEGER argument!"
        sys.exit(1)

    # Data is ready and sanitized
    return points, num_groups


def finalize(groups):
    """
    Write our found groups to groups.json
    :param groups: Dict containing the point groupings
    :return: Void
    """
    with open('groups.json', 'w') as solution:
        json.dump(groups, solution, indent=4)


def hash(point):
    """
    Create a geohash for the given coordinate
    :param point: Dict containing lat/lon fields
    :return: Dict updated with the newly created geohash
    """
    ghash = Geohash.encode(point.get(lat), point.get(lon))
    point[geohash] = ghash
    return point


def distributed_indices(list_len, k):
    """
    Given a list len, return k evenly distributed indices in the list
    :param list_len: Int length of the list
    :param k: Int desired number of distributed indices
    :return: A list of evenly distributed k indices
    """
    return [int(i*list_len/float(k)) for i in range(k)]


def find_anchors(index, anchors):
    """
    Find the indices for the anchors surrounding this index, at most 2
    :param index: Int index of elem in list
    :param anchors: List of ints representing the determined group anchors
    :return: List of ints representing the nearest anchors for the given index
    """

    num_anchors = len(anchors)
    i = 0
    while i < num_anchors - 1:
        # At the beginning of a list
        if index <= anchors[i]:
            return [anchors[i]]
        # A sandwiched case
        elif anchors[i] <= index <= anchors[i+1]:
            if index == anchors[i]:
                return [anchors[i]]
            elif index == anchors[i+1]:
                return [anchors[i+1]]
            else:
                return [anchors[i], anchors[i+1]]
        i += 1
    # At the end of the list
    return [anchors[num_anchors - 1]]


def nearest_neighbor(point, neighbor1, neighbor2):
    """
    Find the nearest neighbor of the provided point
    :param point: Dict containing lat/lon positions
    :param neighbor1: Dict containing lat/lon positions
    :param neighbor2: Dict containing lat/lon positions
    :return: Dict closest to the point
    """
    if neighbor2 is None:
        return neighbor1

    point_lat_lon = (point.get(lat), point.get(lon))
    n1_lat_lon = (neighbor1.get(lat), neighbor1.get(lon))
    n2_lat_lon = (neighbor2.get(lat), neighbor2.get(lon))

    n1_dist = vincenty(point_lat_lon, n1_lat_lon)
    n2_dist = vincenty(point_lat_lon, n2_lat_lon)

    if n1_dist < n2_dist:
        return neighbor1
    else:
        return neighbor2


def group(points, num_groups):
    """
    Group the points by proximity into the specified number of groups
    :param points: List of dicts, containing lat,lon, and id fields
    :param num_groups: Integer specifying the number of groups to cluster points in
    :return: A list of groups (lists), each containing 'near' points
    """

    num_points = len(points)
    # Create hashes for every point
    hashed_points = []
    for point in points:
        hashed_points.append(hash(point))

    """
    # Test scaffolding
    print "Unsorted points:"
    for h in hashed_points:
        print h.get(id), h.get(geohash)
    print ""
    """
    # Sort the points by their hashes.  This provides some degree of clustering
    sorted_points = sorted(hashed_points, key=lambda x: x.get(geohash))

    """
    # Test scaffolding
    print "Sorted Points"
    for h in sorted_points:
        print h.get(id), h.get(geohash)
    """

    # Knowing that the list is now grouped to an extent,
    # We pick out evenly spaced num_groups indices, which we believe
    # to be relatively far from each other
    anchor_indices = distributed_indices(num_points, num_groups)

    # We say that these indices are anchors for each of the groups we'll create
    anchors = [sorted_points[index] for index in anchor_indices]
    groups = {anchor.get(id): [] for anchor in anchors}

    # Go through each point and assign it to a group
    i = 0
    while i < num_points:
        this_point = sorted_points[i]

        # Determine the indices of the nearby anchors
        nearby_anchors = find_anchors(i, anchor_indices)

        # Resolve the points these indexes resolve to
        anchor1 = sorted_points[nearby_anchors[0]]

        # We're not guaranteed a second nearby anchor!
        anchor2 = None
        if len(nearby_anchors) == 2:
            anchor2 = sorted_points[nearby_anchors[1]]

        # Determine the closest anchor
        nearest_anchor = nearest_neighbor(this_point, anchor1, anchor2)

        # We have our mapping, put this point into the according group
        groups.get(nearest_anchor.get(id)).append(this_point.get(id))
        i += 1

    # Now format the groups according to the project spec
    groups = [value for key, value in groups.iteritems()]
    return groups


def run():
    # Init data
    points, num_groups = initialize()
    # Construct the groups
    grouped_points = group(points, num_groups)
    # Write out our results and close up shop
    finalize(grouped_points)

if __name__ == '__main__':
    run()
