from __future__ import annotations

# input: null or area
# każdy kraj zawiera POI. POI to albo cel albo linia.
# osobno jest lista krajów

# jak zmapować kraje do współrzędnych?
# the list of all countries. might be read from a dataset?
# countries = {"Netherlands": {"W":, "E":, "S"}}
#


class Country:
    POIs: [POI]

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
    start: Station
    end: Station

    def __init__(self, points: [Point], start: Station, end: Station):
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

    def distance(self, other: Point):
        self.lat-other.lat

# get coordinates. find out which countries are in range. request countries. return POI
def get_tracks(area: dict):
    # find which countries are in range
    # request countries
    result = {}
    # for each country, filter elements that are within the coordinates
    #
    return result


def get_closest_station(point: dict):
    new_point = Point(point["lat"], point["lon"])
    # se


# track -> trains
def get_trains_over_track():
    return
