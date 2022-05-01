from __future__ import annotations
import math


import math


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

    def __eq__(self, other):
        return (self.location, self.name) == (other.location, other.name)

class Route:
    stops: [Point]
    tracks: [Segment]
    name: str

    def __init__(self, stops: [Point], tracks: [Segment], name: str):
        self.stops = stops
        self.tracks = tracks
        self.name = name


class Segment(POI):
    # List of points is ordered, start and end point are extreme points of the list
    points: [Point]
    description: str
    length: float

    def __init__(self, points: [Point], description: str):
        self.points = points
        self.description = description
        self.calculate_length()

    def __eq__(self, other):
        return (self.points[-1], self.points[0]) == (other.points[-1], other.points[0])

    def __hash__(self):
        return hash((self.points[-1], self.points[0]))

    def get_start(self) -> Point:
        return self.points[0]

    def get_end(self) -> Point:
        return self.points[-1]

    def calculate_length(self):
        start = self.points[0]
        result = 0.0
        for i in range(1, len(self.points)):
            npoint = self.points[i]
            result += start.distance(npoint)
            start = npoint
        self.length = result


class Point:
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def distance(self, other: Point) -> float:
        return math.sqrt(pow(abs(self.lat-other.lat), 2) + pow(abs(self.lon-other.lon), 2))

    def get_array(self) -> [float]:
        return [self.lat, self.lon]

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return (self.lat, self.lon) == (other.lat, other.lon)

    def __hash__(self):
        return hash((self.lat, self.lon))


class Node:
    current: Segment
    previous: Node

    def __init__(self, seg: Segment):
        self.current = seg
        self.previous = None

    def set_previous(self, node: Node):
        self.previous = node

    def __lt__(self, other):
        return True
