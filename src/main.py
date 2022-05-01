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


api.add_resource(ClosestPoint, "/closest_point")
api.add_resource(FuzzySearch, "/fuzzy_search")
app.run(host="0.0.0.0", port=8081, debug=True)

