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


class POI:
    pass


class Station(POI):
    location: Point
    name: str


class Route(POI):
    segments: [Segment]


class Point:
    lat: float
    lon: float


class Segment:
    points: [Point]
    start: Station
    end: Station


# get coordinates. find out which countries are in range. request countries. return POI
def get_tracks(area):
    # countries coordinates: each
    return


# track -> trains
def get_trains_over_track():
    return
