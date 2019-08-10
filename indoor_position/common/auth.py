#!/usr/bin/env python
"""Authentication model.

This model provides two authentication methods: basic authentication,
token authentication.

basic_authentication:
curl -X POST -H "Content-Type: application/json" -u admin:admin http://localhost:5000/tokens
token authentication:
curl -X DELETE -H "Authorization: Bearer token" http://localhost:5000/tokens

"""
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash

from indoor_position.models.user import User
from indoor_position.common.error_handler import BASIC_AUTH_ERROR, TOKEN_AUTH_ERROR, InvalidAPIUsage
basic_auth = HTTPBasicAuth()
#token_auth = HTTPTokenAuth("IndoorPosition")
token_auth = HTTPTokenAuth('Bearer')

@basic_auth.verify_password
def verify_password(username, password):
    """Verify password for basic authentication."""
    if not username or not password:
        return False
    u = User.get_by_user_name(username)
    if u is None or not u.verify_password(password):
        return False
    g.current_user = u
    return True


@basic_auth.error_handler
def password_error():
    """Return a 401 error to a client."""
    raise InvalidAPIUsage(
        error_message="basic authentication required",
        error_code=BASIC_AUTH_ERROR,
        status_code=401
    )


@token_auth.verify_token
def verify_token(token):
    """Token verification."""
    u = User.query.filter_by(_token=token).first()
    if u is None:
        return False
    g.current_user = u
    return True


@token_auth.error_handler
def token_error():
    """Return a 401 error to a client."""
    raise InvalidAPIUsage(
        error_message="token authentication required",
        error_code=TOKEN_AUTH_ERROR,
        status_code=401
    )
