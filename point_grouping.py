import Geohash
import json
import sys
import numpy

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


def group(points, num_groups):
    """
    Group the points by proximity into the specified number of groups
    :param points: List of dicts, containing lat,lon, and id fields
    :param num_groups: Integer specifying the number of groups to cluster points in
    :return: A list of groups (lists), each containing 'near' points
    """

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

    # Split up the sorted points into our groups
    # TODO: Sanitize num_groups
    if num_groups > 0:
        groups = numpy.array_split(sorted_points, num_groups)
    else:
        # If 0 specified groups, it's intuitive to return 1 monolithic group
        groups = numpy.array_split(sorted_points, 1)

    # Currently our groups contain the point objects.
    # We're interested in only returning the corresponding ids though
    # TODO: Form the data while we sort, this is resource heavy...
    groomed_groups = []
    for group in groups:
        groomed_group = []
        for point in group:
            # Each point is now represented by its id
            groomed_group.append(point.get(id))
        groomed_groups.append(groomed_group)

    return groomed_groups


def run():
    # Init data
    points, num_groups = initialize()
    # Construct the groups
    grouped_points = group(points, num_groups)
    # Write out our results and close up shop
    finalize(grouped_points)

if __name__ == '__main__':
    run()
