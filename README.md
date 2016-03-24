## Synopsis

This project aims at solving MakeSpace's Platform Engineer challenge, the [point-grouping-test](https://github.com/makingspace/point-grouping-test).

### Algorithm Overview:
+ Parse our data and assign geohashes to each point
+ Sort the data based on geohashes
+ Split the sorted data into the number of desired groups
+ Perform some necessary formatting
+ Return our groups

### Limitations:
My initial implementation relies on the fact that nearby locations have similar geohashes.  At a macro/international level,
this assumption should potentially not be made and can lead to non-optimized results.  That being said, if we're working at the micro
level, within a city for example, these assumptions facilitate a clean design and produce accurate results.

## Dependencies
To accomplish my solution, I utilized [geopy](https://pypi.python.org/pypi/geopy), [Geohash](https://pypi.python.org/pypi/Geohash/)
and [numpy](http://www.numpy.org/).
These packages are installable via pip:
> pip install -r requirements.txt

## Performance

We're currently in O(n log n) space.  This complexity comes from our use of Python's sorted() tool when sorting our
geohashes.

## Testing
Testing was accomplished by testing each of the helpers, as well as an e2e test on our main group() function.

## TODO
+ Look into formatting our groups while we sort
+ Improve the accuracy at the macro level

## Other Considerations
After doing some research on ways to increase performance, I came across some machine learning resources.  It looks
like one of the more optimal solutions could implement [k-means or DBSCAN clustering](http://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/).
That being said, I've enjoyed learning about geohashes and for now I'm interested in boosting performance utilizing them.
DBSCAN and k-means are tools to keep in mind, and perhaps even implement at a later time.  I just wanted to illustrate my
ability to research a problem and acknowledge the strengths in other solutions, while being proud of my own.

## Thank You!
I would like to sincerely thank the MakeSpace Engineering team for reviewing my candidacy.  Throughout the entire
interview process I've enjoyed learning about the tough problems the team is solving, and am excited to pursue
available opportunities to contribute as well. Thank you for your consideration,

Chris Lyver <br>
(914) 826-7185
