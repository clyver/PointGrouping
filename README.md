## Synopsis

This project aims at solving MakeSpace's Platform Engineer challenge, the [point-grouping-test](https://github.com/makingspace/point-grouping-test).

### Algorithm Overview:
+ Parse our data and assign geohashes to each point
+ Select the points that will anchor each group, which all other points will pivot off of
+ Calculate the closest anchor for every point, and assign groupings
+ Return our groups

### Limitations:
My initial implementation relies on the fact that nearby locations have similar geohashes.  At a macro/international level,
this assumption should potentially not be made and can lead to non-optimized results.  That being said, if we're working at the micro
level, within a city for example, these assumptions facilitate a clean design and produce accurate results.

## Dependencies
To accomplish my solution, I utilized [geopy](https://pypi.python.org/pypi/geopy) and [Geohash](https://pypi.python.org/pypi/Geohash/).
These packages are installable via pip:
> pip install -r requirements.txt

## Performance

We're currently in O(N^2) space.  This comes from the fact that there is a point where we're iterating over the points,
while also iterating over anchors.  There is the potential for the number of points to equal the number of anchors (n*n).

## Testing
Testing was accomplished by testing each of the helpers, as well as and e2e test on our main group() function.

## TODO
+ Try to do better than O(N^2)
+ Improve the accuracy at the macro level
+ Tackle the stretch goal, "distribution"
