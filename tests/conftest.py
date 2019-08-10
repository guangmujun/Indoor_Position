import pytest
from flask import Flask
from webtest import TestApp

from config import TestingConfig
from indoor_position import db as _db
from indoor_position import create_app

@pytest.fixture(scope='module')
def app():
    _app = create_app('testing')
    with _app.test_request_context() as ctx:
        yield _app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def testapp(app):
    return TestApp(app)


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()

