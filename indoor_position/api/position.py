#!/usr/bin/env python

"""
The position service api.

Return position infomation needed for indoor positioning.
"""

from flask_restful import Resource, reqparse, marshal

from indoor_position.models.map import get_adjacent_maps
from .maps import map_record

class PositionAPI(Resource):
    """The position service api."""
    def post(self):
        """Get adjacet maps."""
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('longitude', type=float, required=True)
        post_parser.add_argument('latitude', type=float, required=True)
        post_parser.add_argument('adjacent_distance', type=float)

        args = post_parser.parse_args()
        maps = []
        if args.adjacent_distance:
            maps = get_adjacent_maps(args.longtude, args.latitue, args.adjacent_distance)
        else:
            maps = get_adjacent_maps(args.longtude, args.latitue)
        return {"maps": marshal(maps, map_record)}

