from math import *


def get_distance(lat1, lon1, lat2, lon2):
    def haversin(x):
        return sin(x / 2) ** 2

    return 2 * asin(sqrt(
       haversin(lat2-lat1) +
       cos(lat1) * cos(lat2) * haversin(lon2-lon1))
    )
