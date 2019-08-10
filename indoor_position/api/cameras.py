# coding=UTF-8
from flask_restful import Resource, reqparse, fields, marshal_with, marshal, url_for
from flask import jsonify

from indoor_position.api import api
from indoor_position.models.camera import *
from indoor_position.common.error_handler import *

camera_record = {
    'camera_name': fields.String,
    'map_id': fields.Integer,
    'car_license': fields.String,
    'car_channel': fields.Integer,
    'car_port': fields.Integer,
    'port_stauts': fields.Integer,
    'find_time': fields.Integer,                                                                 
    'uri': fields.Url('api.camera', absolute=True)
}

camera_fields = {
    'camera': camera_record
}

class CameraAPI(Resource):
    """The camera api."""
    @marshal_with(camera_fields)
    def get(self, map_id,camera_id,car_channel,car_port):
        camera = get_camera(car_port)
        if camera is None:
            raise InvalidAPIUsage('get camera fail,car_port  %d no exists!' % car_port, error_code=CAMERA_ERROR)
        return camera

    @marshal_with(camera_fields)
    def post(self,map_id,camera_id,car_channel,car_port):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('camera_name', type=str, location='json',required=True)
        post_parser.add_argument('map_id', type=int, location='json', required=True)
        post_parser.add_argument('car_license', type=str ,location='json',required=False)
        post_parser.add_argument('car_channel', type=str ,location='json',required=True)
        post_parser.add_argument('car_port', type=str ,location='json',required=True)
        post_parser.add_argument('port_stauts', type=str ,location='json',required=True)
        post_parser.add_argument('find_time', type=str ,location='json',required=True)
        args = post_parser.parse_args()
        try:
            camera = create_camera(camera_id,args.camera_name,args.map_id,args.car_license,args.car_channel,args.car_port,args.port_stauts,args.find_time) 			#**************************
            return camera
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)


    @marshal_with(camera_fields)
    def put(self, map_id,camera_id,car_channel,car_port):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('camera_name', type=str, location='json',required=True)
        put_parser.add_argument('map_id', type=int, location='json', required=True)
        put_parser.add_argument('car_license', type=str ,location='json',required=False)
        put_parser.add_argument('car_channel', type=str ,location='json',required=True)
        put_parser.add_argument('car_port', type=str ,location='json',required=True)
        put_parser.add_argument('port_stauts', type=str ,location='json',required=True)
        put_parser.add_argument('find_time', type=str ,location='json',required=True)
        args = put_parser.parse_args()
        try:
            camera = update_camera(camera_id,args.camera_name,args.map_id,args.car_license,args.car_channel,args.car_port,args.port_stauts,args.find_time)
            return camera
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    def delete(self, map_id,camera_id,car_channel,car_port):
        try:
            delete_camera(car_port) 
            r = jsonify('')
            r.status_code = 204
            return r
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)


class CameraListAPI(Resource):
    def get(self):
        cameras = get_all_camera()
        return {'cameras': marshal(cameras, camera_record)}











