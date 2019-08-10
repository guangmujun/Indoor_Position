import pytest

from indoor_position.api import api
from indoor_position.models.map import create_map
from indoor_position.api.maps import MapAPI, MapListAPI
from indoor_position.models.user import User
from indoor_position.api.users import UserAPI, UserListAPI

from indoor_position.common.error_handler import *

@pytest.mark.usefixtures('db')
class TestMapAPI:
    def setup(self):
        self.map1 = create_map(1, 'map1', '/map/test1')
        self.map2 = create_map(2, 'map2', '/map/test2')

    def test_get(self, testapp):
        url = api.url_for(MapAPI, map_id=1)
        rv = testapp.get(url)
        #pytest.set_trace()
        assert rv.json['map']['map_name'] \
               == self.map1.map_name
        assert rv.json['map']['resource_path'] \
               == self.map1.resource_path

        # map_id:3 no exists
        url = api.url_for(MapAPI, map_id=3)
        rv = testapp.get(url, status=400)
        assert rv.json['error_code'] == MAP_ERROR

    def test_post(self, testapp):
        url = api.url_for(MapAPI, map_id=3)
        rv = testapp.post_json(
            url,
            dict(map_name='map3', resource_path='/map/map3'),
            status=200
        )
        assert rv.json['map']['map_name'] == 'map3'
        assert rv.json['map']['resource_path'] == '/map/map3'

        rv = testapp.post_json(
            url,
            dict(map_name='map3', resource_path='/map/map3'),
            status=400
        )
        assert rv.json['error_code'] == MAP_ERROR

    def test_put(self, testapp):
        url = api.url_for(MapAPI, map_id=2)
        rv = testapp.put_json(
            url,
            dict(map_name='map2_update', resource_path='/map/map2_update'),
            status=200
        )
        assert rv.json['map']['map_name'] == 'map2_update'
        assert rv.json['map']['resource_path'] == '/map/map2_update'

        url = api.url_for(MapAPI, map_id=3)
        rv = testapp.put_json(
            url,
            dict(map_mame='map3', resource_path='/maps/map3'),
            status=400
        )
        assert rv.json['error_code'] == MAP_ERROR

    def test_delete(self, testapp):
        url = api.url_for(MapAPI, map_id=1)
        rv = testapp.delete_json(url, status=204)
        # empty content check
        with pytest.raises(ValueError) as ef:
            rv.json
        assert 'No JSON object' in str(ef.value)

        url = api.url_for(MapAPI, map_id=3)
        rv = testapp.delete_json(url, status=400)
        assert rv.json['error_code'] == MAP_ERROR


@pytest.mark.usefixtures('db')
class TestMapTaskAPI:
    def setup(self):
        self.map1 = create_map(1, 'map1', '/map/test1')
        self.map2 = create_map(2, 'map2', '/map/test2')

    def test_get(self, testapp):
        url = api.url_for(MapListAPI)
        rv = testapp.get(url, status=200)
        assert len(rv.json['maps']) == 2


@pytest.mark.usefixtures('db')
class TestUserAPI:
    """The user api unittest."""
    def setup(self):
        self.data1 = {
            "user_id": 1,
            "user_name": "u1",
            "password": "pass1"
        }
        self.user1 = User.create(self.data1)
        self.url1 = api.url_for(UserAPI, user_id=1)

        self.data2 = {
            "user_id": 2,
            "user_name": "u2",
            "password": "pass2"
        }
        self.url2 = api.url_for(UserAPI, user_id=2)

    def test_get(self, testapp):
        rv = testapp.get(self.url1)
        assert rv.json['user']['user_id'] == self.user1.user_id
        assert rv.json['user']['user_name'] == self.user1.user_name

        rv2 = testapp.get(self.url2, status=400)
        assert rv2.json['error_code'] == USER_ERROR

    def test_post(self, testapp):
        rv = testapp.post_json(self.url2, self.data2, status=200)
        assert rv.json['user']['user_id'] == self.data2['user_id']
        assert rv.json['user']['user_name'] == self.data2['user_name']

        rv2 = testapp.post_json(self.url1, self.data1, status=400)
        assert rv2.json['error_code'] == USER_ERROR

    def test_delete(self, testapp):
        rv = testapp.delete(self.url1, status=204)
        with pytest.raises(ValueError) as ef:
            rv.json
        assert 'No JSON object' in str(ef.value)

        rv2 = testapp.delete(self.url2, status=400)
        assert rv2.json['error_code'] == USER_ERROR

    def test_put(self, testapp):
        data1_update = {
            'user_id': 1,
            'user_name': 'u1_update',
            'password': 'pass-update'
        }
        rv = testapp.put_json(self.url1, data1_update, status=200)
        assert rv.json['user']['user_id'] == data1_update['user_id']
        assert rv.json['user']['user_name'] == data1_update['user_name']
        assert self.user1.verifiy_password(data1_update['password'])

        data2_update = {
            'user_id': 2,
            'user_name': 'u2_update'
        }
        rv2 = testapp.put_json(self.url2, data2_update, status=400)
        assert rv2.json['error_code'] == USER_ERROR


@pytest.mark.usefixtures('db')
class TestUserListAPI:
    """The user list api unittest."""
    def setup(self):
        self.data1 = {
            "user_id": 1,
            "user_name": "u1",
            "password": "pass1"
        }
        self.user1 = User.create(self.data1)

        self.data2 = {
            "user_id": 2,
            "user_name": "u2",
            "password": "pass2"
        }
        self.user2 = User.create(self.data2)

        self.url = api.url_for(UserListAPI)

    def test_get(self, testapp):
        rv = testapp.get(self.url, status=200)
        assert len(rv.json['users']) == 2