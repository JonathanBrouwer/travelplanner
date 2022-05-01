from API import API
from util import *

import unittest


class TestClass(unittest.TestCase):

    def test_get_closest_locations(self):
        stations = {Point(0.0, 0.0): "Zero", Point(1.0, 1.0): "One", Point(100.0, 100.0): "Hundred"}
        api = API(stations)
        result = api.get_closest_station({"lat": 0.6, "lng": 0.6})
        assert result == Station(Point(1.0, 1.0), "One")

    def test_get_segment_endpoints(self):
        stations = {Point(0.0, 0.0): "Zero", Point(1.0, 1.0): "One", Point(100.0, 100.0): "Hundred"}
        ways = {1: Segment([Point(0.0, 0.0), Point(0.5, 0.5)], "11"), 2: Segment([Point(0.5, 0.5), Point(3, 3)], "12"),
                3: Segment([Point(3, 3), Point(4, 4)], "13")}
        api = API(stations, ways)
        result = api.get_segment_endpoints({"lat": 0.0, "lng": 0.0})
        print(result)
        assert Point(0.0, 0.0) in result

    def test_get_route_between_stations(self):
        stations = {Point(0.0, 0.0): "Zero", Point(1.0, 1.0): "One", Point(100.0, 100.0): "Hundred"}
        ways = {1: Segment([Point(0.0, 0.0), Point(0.5, 0.5)], "11"), 2: Segment([Point(0.5, 0.5), Point(3, 3)], "12"),
                3: Segment([Point(3, 3), Point(4, 4)], "13")}
        api = API(stations, ways)
        result = api.get_route_between_stations({ "start": {"lat": 0.0, "lng": 0.0}, "end":{"lat": 4.0, "lng": 4.0}})
        print(result)
        assert Segment([Point(0.0, 0.0), Point(0.5, 0.5)], "11") in result


    def test_fuzzy_search(self):
        stations = {Point(0.0, 0.0): "Zero", Point(1.0, 1.0): "One", Point(100.0, 100.0): "Hundred"}
        api = API(stations)
        result = api.fuzzy_search("Hund")
        print(result)
        # assert result == [Station(Point(100.0, 100.0), "Hundred")]