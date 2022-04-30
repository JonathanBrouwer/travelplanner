import API
from util import *

import unittest

class TestClass(unittest.TestCase):

    def test_get_closest_locations(self):
        stations = {Point(0.0, 0.0): "Zero", Point(1.0, 1.0): "One", Point(100.0, 100.0): "Hundred"}
        api = API(stations)
        result = api.get_closest_station(stations.keys()[0])
        assert result