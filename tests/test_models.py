import pytest

from indoor_position.models.map import *
from indoor_position.models.beacon import *
from indoor_position.models.user import User


@pytest.mark.usefixtures('db')
class TestMap:
    def setup(self):
        self.map1 = Map(1, 'test1', '/test/map1', 113.973129, 22.599578)
        self.map1.save()
        self.map2 = Map(2, 'test2', '/test/map2', 114.3311032, 22.6986848)
        self.map2.save()
        
    def test_get_map(self):
        assert self.map1 == get_map(1)
        assert None == get_map(3)

    def test_create_map(self):
        m = create_map(3, 'test3', '/test/map3')
        assert m == get_map(3)
        assert m.map_name == 'test3'
        assert m.resource_path == '/test/map3'

        with pytest.raises(InvalidModelUsage) as ef:
            create_map(2, 'test2', '/test/map2')
        assert ef.value.error_code == MAP_ERROR

    def test_update_map(self):
        with pytest.raises(InvalidModelUsage) as ef:
            update_map(3, 'test3', '/test/map3')
        assert ef.value.error_code == MAP_ERROR
        
        update_map(2, 'test2_update', '/test/map2_update')
        assert self.map2.map_name == 'test2_update'
        assert self.map2.resource_path == '/test/map2_update'

    def test_delete_map(self):
        with pytest.raises(InvalidModelUsage) as ef:
            delete_map(3);
        assert ef.value.error_code == MAP_ERROR

        delete_map(1)
        assert get_map(1) == None

    def test_get_all_map(self):
        assert get_all_map() == [self.map1, self.map2]

    def test_get_adjacent_maps(self):
        data3 = {
                "map_id": 3,
                "map_name": "test3",
                "resource_path": "/maps/test3",
                "longitude": 113.973129,
                "latitude": 22.599578
        }
        data4 = {
                "map_id": 4,
                "map_name": "test4",
                "resource_path": "/maps/test4",
                "longitude": 114.3311032,
                "latitude": 22.6986848
        }

        m3 = Map.create(data3)
        m4 = Map.create(data4)
        

@pytest.mark.usefixtures('db')
class TestBeacon:
    def setup(self):
        map1 = create_map(1, 'test1', '/test/map1')
        map2 = create_map(2, 'test2', '/test/map2')

        beacon = Beacon(1, 2, 3, map1, 1, 2, 3)
        beacon.save()

    def test_get_beacon(self):
        assert Beacon.query.filter_by(beacon_id=1).first() \
               == get_beacon(1)
        assert get_beacon(2) == None

    def test_create_beacon(self):
        b1 = create_beacon(2, 2, 3, 1, 1, 2, 3)
        assert b1 == get_beacon(2)

        with pytest.raises(InvalidModelUsage) as ef:
            b2 = create_beacon(3, 2, 3, 3, 1, 2, 3)
        assert ef.value.error_code == MAP_ERROR

        with pytest.raises(InvalidModelUsage) as ef:
            b3 = create_beacon(1, 2, 3, 1, 1, 2, 3)
        assert ef.value.error_code == BEACON_ERROR

    def test_update_beacon(self):
        b = update_beacon(1, 4, 5, 2, 7, 8, 9)
        assert b.major == 4
        assert b.minor == 5
        assert b.map_id == 2
        assert b.location_x == 7
        assert b.location_y == 8
        assert b.location_z == 9

        with pytest.raises(InvalidModelUsage) as ef:
            b = update_beacon(1, 4, 5, 3, 7, 8, 9)
        assert ef.value.error_code == MAP_ERROR

        with pytest.raises(InvalidModelUsage) as ef:
            b = update_beacon(2, 4, 5, 2, 7, 8, 9)
        assert ef.value.error_code == BEACON_ERROR

    def test_delete_beacon(self):
        delete_beacon(1)
        assert get_beacon(1) == None

        with pytest.raises(InvalidModelUsage) as ef:
            delete_beacon(1)
        assert ef.value.error_code == BEACON_ERROR

    def test_get_all_beacons(self):
        b1 = get_beacon(1)
        b2 = create_beacon(2, 2, 2, 2, 2, 2, 2)
        assert get_all_beacons() == [b1, b2]

    def test_add_adjacent_beacons(self):
        b2 = create_beacon(2, 2, 2, 2, 2, 2, 2)
        b3 = create_beacon(3, 2, 2, 2, 2, 2, 2)
        b4 = create_beacon(4, 2, 2, 2, 2, 2, 2)

        add_adjacent_beacons(2, 3)
        add_adjacent_beacons(2, 4)
        assert set([b3, b4]) == set(b2.to_beacons.all())
        assert [b2] == b3.to_beacons.all()
        assert [b2] == b4.to_beacons.all()
        assert [] == get_beacon(1).to_beacons.all()

        with pytest.raises(InvalidModelUsage) as ef:
            add_adjacent_beacons(5, 2)
        assert ef.value.error_code == BEACON_ERROR

        with pytest.raises(InvalidModelUsage) as ef:
            add_adjacent_beacons(2, 5)
        assert ef.value.error_code == BEACON_ERROR


    def test_get_adjacent_beacons(self):
        b2 = create_beacon(2, 2, 2, 2, 2, 2, 2)
        b3 = create_beacon(3, 2, 2, 2, 2, 2, 2)
        b4 = create_beacon(4, 2, 2, 2, 2, 2, 2)

        add_adjacent_beacons(2, 3)
        add_adjacent_beacons(2, 4)

        assert [b3, b4] == get_adjacent_beacons(2)
        assert [b2] == get_adjacent_beacons(3)
        assert [b2] == get_adjacent_beacons(4)
        assert [] == get_adjacent_beacons(1)

        with pytest.raises(InvalidModelUsage) as ef:
            get_adjacent_beacons(5)
        assert ef.value.error_code == BEACON_ERROR


@pytest.mark.usefixtures('db')
class TestUser:
    """The user model unittest."""
    def setup(self):
        self.password = "12345678"
        self.user = User(
            user_id=1, user_name='test', password=self.password)
        self.user.save()

    def test_password(self):
        with pytest.raises(AttributeError) as ef:
            self.user.password
        assert 'not a readable attribute' in str(ef.value)

        self.user.password = "1234"
        assert self.user.verify_password("1234")
        assert self.user.verify_password("4321") == False

    def test_verify_password(self):
        assert self.user.verify_password(self.password)
        assert self.user.verify_password("87654321") == False

    def test_from_dict_no_partital_update(self):
        data = {
            "user_id": 2,
            "user_name": 'test2',
            "password": '345678'
        }
        self.user.from_dict(data, partial_update=False)
        assert self.user.user_id == data['user_id']
        assert self.user.user_name == data['user_name']
        assert self.user.verify_password(data['password'])

        data2 = {
            "user_id": 3,
            "password": 'tttt'
        }
        with pytest.raises(InvalidModelUsage) as ef:
            self.user.from_dict(data2, partial_update=False)
        # pytest.set_trace()
        assert "[user_name] missed" in ef.value.error_message

    def test_from_dict_partital_update(self):
        data = {
            "user_id": 2,
            "user_name": 'test2'
        }
        self.user.from_dict(data)
        assert self.user.user_id == data['user_id']
        assert self.user.user_name == data['user_name']

    def test_get_by_user_id(self):
        assert User.get_by_user_id(1) == self.user
        assert User.get_by_user_id(2) is None

    def test_create(self):
        data = {
            "user_id": 2,
            "user_name": 'test2',
            "password": 'password123'
        }
        u = User.create(data)
        assert u.user_name == data['user_name']
        assert u.user_id == 2
        assert u.verify_password(data['password'])

        # User already exists
        with pytest.raises(InvalidModelUsage) as ef:
            User.create(data)
        assert 'create user fail, 2 exists!' in ef.value.error_message

        # Field missed
        data2 = {
            "user_id": 3,
            "password": 'none'
        }
        with pytest.raises(InvalidModelUsage) as ef:
            u2 = User.create(data2)
        assert "field [user_name] missed" in ef.value.error_message

    def test_update(self):
        data = {
            'user_id':1,
            'user_name': 'test1_update',
            'password': 'password_update'
        }
        User.update(data)
        assert self.user.user_name == data['user_name']
        assert self.user.verify_password(data['password'])
        assert self.user.verify_password(self.password) == False

        # User no exists
        data = {
            'user_id':2,
            'user_name': 'test2_update'
        }
        with pytest.raises(InvalidModelUsage) as ef:
            User.update(data)
        assert "2 no exists!" in ef.value.error_message

    def test_delete(self):
        User.delete(1)
        assert User.get_by_user_id(1) is None

        with pytest.raises(InvalidModelUsage) as ef:
            User.delete(1)
        assert "1 no exists" in ef.value.error_message

    def test_get_all_users(self):
        self.user2 = User(
            user_id=2, user_name='test2', password="passwd2")
        self.user2.save()
        assert User.get_all_users() == [self.user, self.user2]
