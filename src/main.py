from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

class ClosestPoint(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, location='json')  # added json
        parser.add_argument('lng', type=float, location='json')  # added json
        args = parser.parse_args()

        print("lat: ", args["lat"])
        print("long: ", args["lng"])

        return {'hello': 'world'}


def main():
    app = Flask(__name__)
    CORS(app)

    api = Api(app)

    api.add_resource(ClosestPoint, "/closest_point")

    app.run(host="0.0.0.0", port=8081, debug=True)


if __name__ == '__main__':
    main()