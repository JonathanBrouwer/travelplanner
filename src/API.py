from __future__ import annotations
from util import *
import data_parser
import numpy as np
from sklearn.neighbors import KDTree

<<<<<<< Updated upstream
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
=======

# input: null or area
# każdy kraj zawiera POI. POI to albo cel albo linia.
# osobno jest lista krajów

# jak zmapować kraje do współrzędnych?
# the list of all countries. might be read from a dataset?
# countries = {"Netherlands": {"W":, "E":, "S"}}
#

>>>>>>> Stashed changes

class API:
    station_locations: KDTree
    stations: dict[Point, str]
    stations_reverse: dict[str, Point]
    data: [[float]]

    @classmethod
    def load(cls):
        stations = data_parser.load_full()
        return cls(stations.stations)

    def __init__(self, stations):
        self.stations = stations
        self.stations_reverse = {}
        for (k, v) in stations.items():
            self.stations_reverse[v] = k

        self.data = []  # to make the KDTree
        for value in stations:
            self.data.append(value.get_array())
        self.station_locations = KDTree(np.array(self.data))

    def get_closest_station(self, point: dict) -> Station:
        ind = self.station_locations.query([[point["lat"], point["lng"]]], return_distance=False)
        point = self.data[ind[0][0]]
        point = Point(point[0], point[1])
        result = self.stations.get(point)
        result = Station(point, result)
        return result

    def fuzzy_search(self, name: str) -> [Station]:
        return [Station(self.stations_reverse[x[0]], x[0]) for x in process.extract(name, self.stations.values(), limit=10)]