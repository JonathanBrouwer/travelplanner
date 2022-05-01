from __future__ import annotations

import itertools

import pygtrie

from util import *
import data_parser
import numpy as np
from sklearn.neighbors import KDTree

cool_data: any

class API:
    station_locations: KDTree
    stations: dict[Point, str]
    stations_reverse: dict[str, Point]
    data: [[float]]

    @classmethod
    def load(cls):
        data = data_parser.load_full(area="eu")
        global cool_data
        cool_data = data
        return cls(data.stations)

    def __init__(self, stations: dict[Point, str]):
        self.stations = stations
        self.stations_reverse = {}
        for (k, v) in stations.items():
            self.stations_reverse[v] = k

        self.trie: pygtrie.CharTrie = pygtrie.CharTrie()
        for station in stations.values():
            station: str
            self.trie[station.lower()] = station

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
        name = name.lower()
        if len(name) < 2:
            results = []
        else:
            try:
                results = list(itertools.islice(self.trie.itervalues(prefix=name), 10))
            except:
                results = []
        return [Station(self.stations_reverse[res], res) for res in results]
