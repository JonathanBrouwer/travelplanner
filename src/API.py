from __future__ import annotations
from Util import *
import data_parser
from sklearn.neighbors import KDTree

# input: null or area
# każdy kraj zawiera POI. POI to albo cel albo linia.
# osobno jest lista krajów

# jak zmapować kraje do współrzędnych?
# the list of all countries. might be read from a dataset?
# countries = {"Netherlands": {"W":, "E":, "S"}}
#




class API:
    station_locations: KDTree
    stations: dict[Point, str]

    def __init__(self):
        data = data_parser.get_stations()
        for key, value in data:
            pass
        self.station_locations = KDTree()


    @staticmethod
    def get_closest_station(point: dict) -> Station:
        new_point = Point(point["lat"], point["lon"])
        stations = data_parser.get_stations()
        result = Station(Point(-1, -1), "")
        distance = new_point.distance(result.location)

        # exhaustive search for closest station
        for station in stations:
            new_dist = new_point.distance(station.location)
            if new_dist < distance:
                distance = new_dist
                result = station
        return result


# track -> trains
def get_trains_over_track():
    return
