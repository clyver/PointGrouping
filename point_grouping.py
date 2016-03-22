import Geohash
from geopy.distance import vincenty
import json
import sys
import math

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
        json_data = open('./initialExperiments/sample_points.json').read()
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


def hash(point_lat, point_lon, point_id):
    """
    Create a geohash for the given coordinate
    :param point_lat: Float representing a latitude value
    :param point_lon: Float representing a longitude value
    :param point_id: String representing a unique identifier for this point
    :return: Dict containing the input parameters, plus the newly created geohash
    """
    return {geohash: Geohash.encode(point_lat, point_lon),
            lat: point_lat,
            lon: point_lon,
            id: point_id}


def distributed_indices(list_len, k):
    """

    :param list_len: Int length of the list
    :param : Int desired number of distributed indicies
    :return: A list of evenly distributed k indices
    """
    return [int(i*list_len/float(k)) for i in range(k)]


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
        point_lat = point.get(lat)
        point_lon = point.get(lon)
        point_id = point.get(id)
        hashed_points.append(hash(point_lat, point_lon, point_id))

    # Sort the points by their hashes.  This provides some degree of clustering
    sorted_hashes = sorted(hashed_points, key=lambda x: x.get(geohash))
    for h in sorted_hashes:
        print h.get(id), h.get(geohash)
    

if __name__ == '__main__':
    points, num_groups = initialize()
    group(points, num_groups)