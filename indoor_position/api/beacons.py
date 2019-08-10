from flask_restful import Resource, reqparse, fields, marshal_with, marshal

from indoor_position.models.beacon import *
from indoor_position.common.error_handler import *

beacon_record = {
    'major': fields.Integer,
    'minor': fields.Integer,
    'map_id': fields.Integer,
    'uri': fields.Url('api.beacon', absolute=True)
}

beacon_fields = {
    'beacon': beacon_record
}

class BeaconAPI(Resource):
    @marshal_with(beacon_fields)
    def get(self, beacon_id):
        beacon = get_beacon(beacon_id)
        if beacon is None:
            raise InvalidAPIUsage("get beacon fail: %d no exists!" % beacon_id, status_code=412) 
        return beacon

    @marshal_with(beacon_fields)
    def post(self, beacon_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('major', type=int, location='json', required=True)
        post_parser.add_argument('minor', type=int, location='json', required=True)
        post_parser.add_argument('map_id', type=int, location='json', default=True)

        args = post_parser.parse_args()
        try:
            beacon = create_beacon(beacon_id, args.major, args.minor, args.map_id)
            return beacon
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    
    @marshal_with(beacon_fields)
    def put(self, beacon_id):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('major', type=int, location='json')
        put_parser.add_argument('minor', type=int, location='json')
        put_parser.add_argument('map_id', type=int, location='json')
        args = put_parser.parse_args()

        try:
            beacon = update_beacon(beacon_id, args.major, args.minor, args.map_id)
            return beacon
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    def delete(self, beacon_id):
        try:
            r = delete_beacon(beacon_id)
            r = jsonify('')
            r.status_code = 204
            return r
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)


class BeaconListAPI(Resource):
    def get(self):
        beacons = get_all_beacons()
        return {'beacons': marshal(beacons, beacon_record)}


