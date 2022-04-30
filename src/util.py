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

    def __init__(self, points: [Point], description: str):
        self.points = points
        self.description = description


class Point:
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def distance(self, other: Point) -> float:
        return math.sqrt(pow(abs(self.lat-other.lat), 2) + pow(abs(self.lon-other.lon), 2))

    def get_array(self) -> [float]:
        return {self.lat, self.lon}

    def __hash__(self):
        return hash((self.lat, self.lon))