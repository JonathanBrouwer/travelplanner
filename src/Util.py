from __future__ import annotations

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