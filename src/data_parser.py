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

if __name__ == '__main__':
    stations = get_stations(area="nl")
    tracks = get_tracks(area="nl")
    print(len(tracks))