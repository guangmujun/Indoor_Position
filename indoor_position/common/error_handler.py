from flask import jsonify
from enum import Enum

from indoor_position.api import api_blueprint 

UNKNOWN_ERROR = 0
MAP_ERROR = 1000
BEACON_ERROR = 1001
CAMERA_ERROR = 1002
USER_ERROR = 1003
BASIC_AUTH_ERROR = 1004
TOKEN_AUTH_ERROR = 1005

ERROR_CODE_DICT = {
    UNKNOWN_ERROR: 'Unknown Error',
    MAP_ERROR: 'Map Error',
    BEACON_ERROR: 'Beacon Error',
    CAMERA_ERROR: 'Camera Error',
    USER_ERROR: 'User Error',
    BASIC_AUTH_ERROR: 'Basic Auth Error',
    TOKEN_AUTH_ERROR: 'Token Auth Error'
}

class InvalidAPIUsage(Exception):
    def __init__(self, error_message, error_code=None, status_code=400, payload=None):
        Exception.__init__(self)
        if error_code in ERROR_CODE_DICT:
            self.error_code = error_code
        else:
            self.error_code = 0
        self.error_message = "{0}: {1}".format(ERROR_CODE_DICT[self.error_code], error_message)
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error_message'] = self.error_message
        rv['error_code'] = self.error_code
        return rv
    

@api_blueprint.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class InvalidModelUsage(Exception):
    def __init__(self, error_msg, error_code):
        self.error_message = error_msg
        self.error_code = error_code

    
