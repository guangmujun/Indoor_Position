"""The token api.
"""

from flask import g, jsonify
from flask_restful import Resource

from indoor_position.common.auth import basic_auth, token_auth

class TokenAPI(Resource):
    """The token api."""
    @basic_auth.login_required
    def post(self):
        """Return a user token."""
        if g.current_user.token is None:
            g.current_user.generate_token()
        return jsonify({'token': g.current_user.token})

    @token_auth.login_required
    def delete(self):
        """Delete a user token."""
        g.current_user.token = None
        return '', 204
