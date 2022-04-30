from __future__ import annotations
from util import *
import data_parser
import numpy as np
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
    data: [[float]]

    @classmethod
    def load(cls):
        stations = data_parser.get_stations()
        return cls(stations)

    def __init__(self, stations):
        self.stations = stations
        self.data = []  # to make the KDTree
        for value in stations:
            self.data.append(value.get_array())
        self.station_locations = KDTree(np.array(self.data))

    def get_closest_station(self, point: dict) -> Station:
        new_point = Point(point["lat"], point["lgn"])
        ind = self.station_locations.query([[point["lat"], point["lgn"]]], return_distance=False)
        point = self.data[ind[0][0]]
        point = Point(point[0], point[1])
        result = self.stations.get(point)
        result = Station(point, result)
        return result
