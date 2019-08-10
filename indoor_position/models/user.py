import binascii
import os

from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash

from indoor_position import db
from indoor_position.common.utils import timestamp
from indoor_position.common.error_handler import InvalidModelUsage, USER_ERROR

class User(db.Model):
    """The user model."""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    user_name = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    _token = db.Column(db.String(64), nullable=True, unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        self.token = None  # if user is changing password, also revoke token

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        """Create a 64 char long randomly generated token."""
        self.token = binascii.hexlify(os.urandom(32)).decode('utf-8')
        return self.token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
        self.save()

    def from_dict(self, data, partial_update=True):
        """Import user data from a dict."""
        for f in ['user_id', 'user_name', 'password']:
            try:
                setattr(self, f, data[f])
            except KeyError:
                if not partial_update:
                    raise InvalidModelUsage(
                        "change user infomation from dict fail, field [%s] missed" % f,
                        USER_ERROR)

    def save(self):
        """Save user information to db."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_user_id(uid):
        """Get user by user_id."""
        return User.query.filter_by(user_id=uid).first()

    @staticmethod
    def create(data):
        """Create a new user."""
        if 'user_id' not in data:
            raise InvalidModelUsage('user_id field missed!', USER_ERROR)
        user_id = data['user_id']

        u = User.get_by_user_id(user_id)
        if u:
            raise InvalidModelUsage('create user fail, %d exists!' % user_id, USER_ERROR)
        user = User()
        user.from_dict(data, partial_update=False)
        user.save()
        return user
    
    @staticmethod
    def update(data):
        """Update user information."""
        if 'user_id' not in data:
            raise InvalidModelUsage('user_id field missed!', USER_ERROR)
        user_id = data['user_id']

        u = User.get_by_user_id(user_id)
        if u is None:
            raise InvalidModelUsage('update user fail, %d no exists!' % user_id, USER_ERROR)
        u.from_dict(data)
        u.save()
        return u

    @staticmethod
    def delete(user_id):
        """Delete user."""
        u = User.get_by_user_id(user_id)
        if u is None:
            raise InvalidModelUsage('delete user fail, %d no exists!' % user_id, USER_ERROR)
        db.session.delete(u)
        db.session.commit()

    @staticmethod
    def get_all_users():
        """Get all users."""
        users = User.query.all()
        return users

    @staticmethod
    def get_by_user_name(username):
        return User.query.filter_by(user_name=username).first()
