from flask_restful import Resource, reqparse, fields, marshal_with, marshal, url_for
from flask import jsonify

from indoor_position.api import api
from indoor_position.models.map import *
from indoor_position.common.error_handler import *
from indoor_position.common.auth import basic_auth, token_auth
from indoor_position.api.download import DownloadAPI

class ResourcePath(fields.Raw):
    def format(self, file_name):
        return api.url_for(DownloadAPI, file_name=file_name, _external=True)

map_record = {
    'map_name': fields.String,
    'resource_path': ResourcePath,
    'uri': fields.Url('api.map', absolute=True)
}

map_fields = {
    'map': map_record 
}

class MapAPI(Resource):
    """The map api."""
#    decorators = [
#        basic_auth.login_required
#    ]

    @marshal_with(map_fields)
    def get(self, map_id):
        map = get_map(map_id)
        if map is None:
            raise InvalidAPIUsage('get map fail, %d no exists!' % map_id, error_code=MAP_ERROR)
        return map

    @marshal_with(map_fields)
    def post(self, map_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('map_name', type=str, required=True)
        #post_parser.add_argument('resource_path', type=str, location='json', required=True)
        args = post_parser.parse_args()
        try:
            resource_path = "%d.tar.gz" % map_id
            map = create_map(map_id, args.map_name, resource_path)
            return map
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    @marshal_with(map_fields)
    def put(self, map_id):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('map_name', type=str, location='json')
        #put_parser.add_argument('resource_path', type=str, location='json')
        args = put_parser.parse_args()
        try:
            map = update_map(map_id, args.map_name, None)
            return map
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    def delete(self, map_id):
        try:
            delete_map(map_id) 
            r = jsonify('')
            r.status_code = 204
            return r
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)


class MapListAPI(Resource):
    def get(self):
        maps = get_all_map()
        return {'maps': marshal(maps, map_record)}
