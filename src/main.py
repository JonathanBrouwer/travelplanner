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


api.add_resource(ClosestPoint, "/closest_point")
app.run(host="0.0.0.0", port=8081, debug=True)

