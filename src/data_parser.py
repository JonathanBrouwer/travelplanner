import xml.etree.ElementTree as ET

from src.API import Station, Point


def get_stations() -> [Station]:
    mytree = ET.parse('../data/nl_railway_stations_final.xml')
    root = mytree.getroot()

    stations = []
    for node in root.findall("node"):
        lat = node.attrib["lat"]
        long = node.attrib["lon"]
        names = [tag.attrib["v"] for tag in node.findall("tag") if tag.attrib["k"] == "name"]
        name = names[0] if len(names) > 0 else ""
        stations.append(Station(Point(lat, long), name))

    return stations


if __name__ == '__main__':
    get_stations()