import os

from flask import send_from_directory, abort
from flask_restful import Resource

from config import MAP_DATA_DIR

class DownloadAPI(Resource):
    """The file download api."""
    def get(self, file_name):
        print file_name
        print os.path.join(MAP_DATA_DIR, file_name)
        if os.path.isfile(os.path.join(MAP_DATA_DIR, file_name)):
            return send_from_directory(MAP_DATA_DIR, file_name, as_attachment=True)
        abort(404)