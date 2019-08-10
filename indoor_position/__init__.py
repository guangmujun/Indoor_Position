from flask_restful import Api
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

from config import config 


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get(
                'INDOOR_POSITION_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize flask extensions
    db.init_app(app)
    
    # Register RESTful api
    from api import api_blueprint
    app.register_blueprint(api_blueprint)
    return app

from indoor_position import models
from indoor_position import api


