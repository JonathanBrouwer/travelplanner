import xml.etree.ElementTree as ET

from src.API import Point, Segment

def get_stations(area="nl") -> dict[Point, str]:
    mytree = ET.parse("../data/" + area + "_railway_stations.xml")
    root = mytree.getroot()

    stations = {}
    for node in root.findall("node"):
        lat = float(node.attrib["lat"])
        long = float(node.attrib["lon"])
        names = [tag.attrib["v"] for tag in node.findall("tag") if tag.attrib["k"] == "name"]
        name = names[0] if len(names) > 0 else ""
        stations[Point(lat, long)] = name

    return stations

def get_tracks(area="nl") -> [Segment]:
    mytree = ET.parse("../data/" + area + "_railway_tracks.xml")
    root = mytree.getroot()

    points: dict[int, Point] = {}
    for node in root.findall("node"):
        idd = int(node.attrib["id"])
        lat = float(node.attrib["lat"])
        long = float(node.attrib["lon"])
        points[idd] = Point(lat, long)

    segments: [Segment] = []
    for way in root.findall("way"):
        nodes = [points[int(nd.attrib["ref"])] for nd in way.findall("nd")]
        descriptions = [tag.attrib["v"] for tag in way.findall("tag") if tag.attrib["k"] == "description"]
        description = descriptions[0] if len(descriptions) > 0 else ""

        segments.append(Segment(nodes, description))

    return segments


def load_full(area="nl"):
    mytree = ET.parse("../data/" + area + "_railway_tracks.xml")
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

    ways: [Segment] = []
    for way in root.findall("way"):
        nodes_in_way = [nodes[int(nd.attrib["ref"])] for nd in way.findall("nd")]
        descriptions = [tag.attrib["v"] for tag in way.findall("tag") if tag.attrib["k"] == "description"]
        description = descriptions[0] if len(descriptions) > 0 else ""

        ways.append(Segment(nodes_in_way, description))

    for route in root.findall("relation"):
        pass


    pass


if __name__ == '__main__':
    load_full(area="nl")