from __future__ import annotations
from util import *
import data_parser
import numpy as np
from sklearn.neighbors import KDTree



class API:
    station_locations: KDTree
    stations: dict[Point, str]
    data: [[float]]

    @classmethod
    def load(cls):
        data = data_parser.load_full(area="nl")
        stations = data.stations
        return cls(stations)

    def __init__(self, stations):
        self.stations = stations
        self.data = []  # to make the KDTree
        for value in stations:
            self.data.append(value.get_array())
        self.station_locations = KDTree(np.array(self.data))

    def get_closest_station(self, point: dict) -> Station:
        new_point = [[point["lat"], point["lgn"]]]
        ind = self.station_locations.query(new_point, return_distance=False)
        point = self.data[ind[0][0]]
        point = Point(point[0], point[1])
        result = self.stations.get(point)
        result = Station(point, result)
        return result
