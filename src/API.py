from __future__ import annotations
import math
import data_parser
from sklearn.neighbors import KDTree

# input: null or area
# każdy kraj zawiera POI. POI to albo cel albo linia.
# osobno jest lista krajów

# jak zmapować kraje do współrzędnych?
# the list of all countries. might be read from a dataset?
# countries = {"Netherlands": {"W":, "E":, "S"}}
#

class CountryData:
    name: str
    extremes: dict


class Country:
    POIs: [POI]
    data: CountryData

    def __init__(self, POIlist: [POI]):
        self.POIs = POIlist


class POI:
    pass


class Station(POI):
    location: Point
    name: str

    def __init__(self, point: Point, name: str):
        self.location = point
        self.name = name


class Segment(POI):
    points: [Point]
    start: Point
    end: Point

    def __init__(self, points: [Point], start: Point, end: Point):
        self.points = points
        self.start = start
        self.end = end


class Route:
    segments: [Segment]


class Point:
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def distance(self, other: Point) -> float:
        return math.sqrt(pow(abs(self.lat-other.lat), 2) + pow(abs(self.lon-other.lon), 2))

    def __hash__(self):
        return hash((self.lat, self.lon))


class API:
    station_locations: KDTree
    stations: dict[Point, str]

    def __init__(self):
        self.stations = KDTree()


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
