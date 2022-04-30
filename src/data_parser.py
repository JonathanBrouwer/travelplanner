import xml.etree.ElementTree as ET

from src.API import Point, Segment
from src.util import Route

class Data:
    stations: dict[Point, str]
    nodes: dict[int, Point]
    ways: dict[int, Segment]
    routes: [Route]

    def __init__(self, stations, nodes, ways, routes):
        self.stations = stations
        self.nodes = nodes
        self.ways = ways
        self.routes = routes

def load_full(area="nl") -> Data:
    mytree = ET.parse("../data/" + area + "_full.xml")
    root = mytree.getroot()

    stations: dict[Point, str] = {}
    nodes: dict[int, Point] = {}
    for node in root.findall("node"):
        idd = int(node.attrib["id"])
        lat = float(node.attrib["lat"])
        long = float(node.attrib["lon"])
        point = Point(lat, long)
        nodes[idd] = point

        tags = node.findall("tag")
        is_station = len([tag for tag in tags if tag.attrib["k"] == "railway" and (tag.attrib["v"] == "station" or tag.attrib["v"] == "halt")]) > 0
        if is_station:
            names = [tag.attrib["v"] for tag in node.findall("tag") if tag.attrib["k"] == "name"]
            name = names[0] if len(names) > 0 else ""
            stations[point] = name

    ways: dict[int, Segment] = {}
    for way in root.findall("way"):
        idd = int(way.attrib["id"])
        nodes_in_way = [nodes[int(nd.attrib["ref"])] for nd in way.findall("nd")]
        descriptions = [tag.attrib["v"] for tag in way.findall("tag") if tag.attrib["k"] == "description"]
        description = descriptions[0] if len(descriptions) > 0 else ""

        ways[idd] = Segment(nodes_in_way, description)

    routes: [Route] = []
    for route in root.findall("relation"):
        stops = [nodes[int(member.attrib["ref"])] for member in route.findall("member") if member.attrib["type"] == "node" and int(member.attrib["ref"]) in nodes]
        tracks = [ways[int(member.attrib["ref"])] for member in route.findall("member") if member.attrib["type"] == "way" and int(member.attrib["ref"]) in ways]

        names = [tag.attrib["v"] for tag in route.findall("tag") if tag.attrib["k"] == "name"]
        name = names[0] if len(names) > 0 else ""

        routes.append(Route(stops, tracks, name))

    return Data(stations, nodes, way, routes)

if __name__ == '__main__':
    load_full(area="nl")