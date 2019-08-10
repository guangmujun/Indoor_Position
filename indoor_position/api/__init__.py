# coding=UTF-8
from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

from maps import MapAPI, MapListAPI
from cameras import CameraAPI,CameraListAPI
from beacons import BeaconAPI, BeaconListAPI
from users import UserAPI, UserListAPI
from tokens import TokenAPI
from download import DownloadAPI

api.add_resource(MapAPI, '/maps/<int:map_id>', endpoint='map')
api.add_resource(MapListAPI, '/maps', endpoint='maps')
api.add_resource(CameraAPI, '/cameras/<int:map_id>/<int:camera_id>/<int:car_channel>/<int:car_port>', endpoint='camera')
api.add_resource(CameraListAPI, '/cameras', endpoint='cameras')
api.add_resource(BeaconAPI, '/beacons/<int:beacon_id>', endpoint='beacon')
api.add_resource(BeaconListAPI, '/beacons', endpoint='beacons')
api.add_resource(UserAPI, '/users/<int:user_id>', endpoint='user')
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(TokenAPI, '/tokens', endpoint='tokens')
api.add_resource(DownloadAPI, '/download/<string:file_name>', endpoint='download')
