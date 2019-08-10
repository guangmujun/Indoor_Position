from math import radians, cos, sin, asin, sqrt, fabs
import time

def timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())


EARTH_RADIUS = 6371
def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earch."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine 
    dlon = fabs(lon1 - lon2)
    dlat = fabs(lat1 - lat2)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * asin(sqrt(a)) * EARTH_RADIUS 

#lat1,lon1 = (22.599578, 113.973129)
#lat2,lon2 = (22.6986848, 114.3311032)
#
#print haversine(lat1, lon1, lat2, lon2)
