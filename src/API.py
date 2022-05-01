from __future__ import annotations

import itertools

import pygtrie


import heapq
import math
import copy

from util import *
import data_parser
import numpy as np
from sklearn.neighbors import KDTree

cool_data: any

class API:
    station_locations: KDTree
    stations: dict[Point, str]
    station_data: [[float]]
    segment_endpoints: KDTree
    segments: dict[Point, [Segment]]
    segment_data: [[float]]
    stations_reverse: dict[str, Point]
    data: [[float]]

    @classmethod
    def load(cls):
        data = data_parser.load_full(area="eu")
        global cool_data
        cool_data = data
        return cls(data.stations)

    def __init__(self, stations: dict[Point, str], ways: dict[int, Segment] = None):
        self.stations = stations
        self.station_data = []  # to make the KDTree
        self.stations_reverse = {}
        for (k, v) in stations.items():
            self.stations_reverse[v] = k

        self.trie: pygtrie.CharTrie = pygtrie.CharTrie()
        for station in stations.values():
            station: str
            self.trie[station.lower()] = station
        for value in stations:
            self.station_data.append(value.get_array())
        self.station_locations = KDTree(np.array(self.station_data))
        if ways is not None:
            self.segments = {}
            self.segment_data = []
            print(len(ways.values()))
            for value in ways.values():
                start = value.get_start()
                end = value.get_end()
                if start not in self.segments.keys():
                    self.segments[start] = [value]
                    self.segment_data.append(start.get_array())
                else:
                    self.segments[start].append(value)
                if end not in self.segments.keys():
                    self.segments[end] = [value]
                    self.segment_data.append(end.get_array())
                else:
                    self.segments[end].append(value)

            self.segment_endpoints = KDTree(np.array(self.segment_data))

    def get_closest_station(self, point: dict) -> Station:
        new_point = [[point["lat"], point["lng"]]]
        ind = self.station_locations.query(new_point, return_distance=False)
        point = self.station_data[ind[0][0]]
        point = Point(point[0], point[1])
        result = self.stations.get(point)
        result = Station(point, result)
        return result

    def get_segment_endpoints(self, point: dict) -> [Point]:
        new_point = [[point["lat"], point["lng"]]]
        ind = self.segment_endpoints.query_radius(new_point, r=0.001, return_distance=False)
        ind = ind[0]
        result = []
        for i in ind:
            point = self.segment_data[i]
            pointt = Point(point[0], point[1])
            result.append(pointt)
        return result

    def make_set(self, node:Node) -> set[Segment]:
        result = set()
        result.add(node.current)
        while node.previous is not None:
            node = node.previous
            result.add(node.current)
        return result



    def get_route_between_stations(self, data: dict) -> set[Segment]:
        start = data["start"]
        end = data["end"]
        end_point = [[end["lat"], end["lng"]]]
        end_as_point = Point(end_point[0][0], end_point[0][1])
        heuristic = lambda x: x.distance(end_as_point)  # heuristic function
        # list of: heuristic value, actual point, total distance from start, set of segments
        start_points = list(map(lambda x: (heuristic(x), x, 0.0, Node(None)), self.get_segment_endpoints(start)))
        heapq.heapify(start_points)
        end_segments = self.get_segment_endpoints(end)
        end_points = set()
        for seg in end_segments:
            end_points.add(seg)
        current = heapq.heappop(start_points)
        while current[1] not in end_points:
            new_segs = self.segments[current[1]]
            for seg in new_segs:
                s = Node(seg)
                s.set_previous(current[3])
                if seg.get_start() != current[1]:
                    heapq.heappush(start_points, (heuristic(seg.get_start())+seg.length, seg.get_start(), current[2]+seg.length, s))
                else:
                    heapq.heappush(start_points, (heuristic(seg.get_end())+seg.length, seg.get_end(), current[2]+seg.length, s))
            current = heapq.heappop(start_points)
        return self.make_set(current[3])
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
