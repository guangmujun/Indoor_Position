from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, marshal

from indoor_position.models.user import User 
from indoor_position.common.error_handler import InvalidModelUsage, InvalidAPIUsage, USER_ERROR

user_record = {
        'user_id': fields.Integer,
        'user_name': fields.String,
        'uri': fields.Url('api.user', absolute=True),
        'created_at': fields.Integer,
        'updated_at': fields.Integer
}

user_fields = {
        'user': user_record
}

class UserAPI(Resource):
    """The user api."""
    @marshal_with(user_fields)
    def get(self, user_id):
        """Return a user."""
        u = User.get_by_user_id(user_id)
        if u is None:
            raise InvalidAPIUsage(
                    'get user fail, %d no exists!' % user_id, error_code=USER_ERROR)
        return u
    
    @marshal_with(user_fields)
    def post(self, user_id):
        """Create a user."""
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('user_name', type=str, location='json', required=True)
        post_parser.add_argument('password', type=str, location='json', required=True)
        args = post_parser.parse_args()
        try:
            data = UserAPI.args2dict(user_id, args)
            u = User.create(data)
            return u
        except InvalidModelUsage as e: 
            raise InvalidAPIUsage(e.error_message, e.error_code)

    def delete(self, user_id):
        """Delete a user."""
        try:
            User.delete(user_id)
            r = jsonify('')
            r.status_code = 204
            return r
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    @marshal_with(user_fields)
    def put(self, user_id):
        """Update a user."""
        # parse request
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('user_name', type=str, location='json')
        put_parser.add_argument('password', type=str, location='json')
        args = put_parser.parse_args()
        try:
            data = UserAPI.args2dict(user_id, args)
            u = User.update(data)
            return u
        except InvalidModelUsage as e:
            raise InvalidAPIUsage(e.error_message, e.error_code)

    @staticmethod
    def args2dict(user_id, args):
        d = {}
        d['user_id'] = user_id
        if args.user_name is not None:
            d['user_name'] = args.user_name
        if args.password is not None:
            d['password'] = args.password
        return d

class UserListAPI(Resource):
    def get(self):
        users = User.get_all_users()
        return {'users': marshal(users, user_record)}