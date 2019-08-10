import platform
import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))

# Set map data directory according to platform service ran
sysstr = platform.system()
if sysstr == "Windows":
    MAP_DATA_DIR = os.path.join(basedir, 'indoor_position\static\data\maps')
elif sysstr == "Linux" or sysstr == "Darwin":
    MAP_DATA_DIR = os.path.join(basedir, 'indoor_position/static/data/maps')
else:
    print "map data directory init failed: unknown system [%s]!" % sysstr
    sys.exit(1)

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'indoor-position-wang'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'indoor_position.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/indoor_position'


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
