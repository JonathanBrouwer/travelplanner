from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from API import API

app = Flask(__name__)
CORS(app)
api = Api(app)
interface = API.load()

class ClosestPoint(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, location='json')  # added json
        parser.add_argument('lng', type=float, location='json')  # added json
        args = parser.parse_args()
        station = interface.get_closest_station(args)

        return {
            "lat": station.location.lat,
            "lng": station.location.lon,
            "name": station.name,
        }

class FuzzySearch(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()
        stations = interface.fuzzy_search(args["name"])

        return {
            "result": [{"name": station.name, "lng": station.location.lon, "lat": station.location.lat} for station in stations]
        }


class Route(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat1', type=float, location='json')
        parser.add_argument('lng1', type=float, location='json')
        parser.add_argument('lat2', type=float, location='json')
        parser.add_argument('lng2', type=float, location='json')
        args = parser.parse_args()

        print(args)

        res = interface.get_route_between_stations({
            "start": {
                "lat": args["lat1"],
                "lng": args["lng1"],
            },
            "end": {
                "lat": args["lat2"],
                "lng": args["lng2"],
            }
        })

        print(res)

        return {
            "segments": [
                [[p.lat, p.lon] for p in i.points]
                for i in res
                if i is not None
            ]
        }


api.add_resource(ClosestPoint, "/closest_point")
api.add_resource(Route, "/route")
api.add_resource(FuzzySearch, "/fuzzy_search")
app.run(host="0.0.0.0", port=8081, debug=True)

