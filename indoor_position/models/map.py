from indoor_position import db
from indoor_position.common.error_handler import *
from indoor_position.common.utils import haversine


class Map(db.Model):
    __tablename__ = 'maps'
    map_id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.Text)
    resource_path = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
#    location = db.relationship('Location', backref='map', lazy='dynamic', uselist=False)
    beacons = db.relationship('Beacon', backref='map', lazy='dynamic')
    cameras = db.relationship('Camera', backref='map', lazy='dynamic')

    def __init__(self, map_id=None, map_name=None, resource_path=None, longitude=None, latitude=None, beacons=None,cameras=None):
        self.map_id = map_id
        self.map_name = map_name
        self.resource_path = resource_path
        self.longitude = longitude
        self.latitude = latitude
        if beacons:
            for b in beacons:
                self.beacons.append(b)
        if cameras:
            for c in cameras:
                self.cameras.append(c)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def from_dict(self, data, partial_update=True):
        """Import map data from a dict."""
        fs = ['map_id', 'map_name', 'resource_path', 'longitude', 'latitude']
        for f in fs:
            try:
                setattr(self, f, data[f])
            except KeyError:
                if not partial_update:
                    raise InvalidModelUsage(
                            "change map information from dict fail, field [%s] missed!" % f,
                            MAP_ERROR)

    @staticmethod
    def create(data):
        """Create a map."""
        if "map_id" not in data:
            raise InvalidModelUsage('map_id field missed!', MAP_ERROR)
        map_id = data['map_id']

        map = Map.get_by_map_id(map_id)
        if map:
            raise InvalidModelUsage('create map fail, %d exists!' % map_id, MAP_ERROR)
        map = Map()
        map.from_dict(data, partial_update=False)
        map.save()
        return map

    @staticmethod
    def get_by_map_id(map_id):
        map = Map.query.filter_by(map_id=map_id).first()
        return map

def get_map(map_id):
    map = Map.query.filter_by(map_id=map_id).first()
    return map


def create_map(map_id, map_name, resource_path):
    '''Create map record. If map_id exists, raise MAP_ERROR
    '''
    # check if record exists
    map = get_map(map_id)
    if map is not None:
        raise InvalidModelUsage('create map fail, %d exists!' % map_id, MAP_ERROR)

    map = Map(map_id, map_name, resource_path)
    db.session.add(map)
    db.session.commit()
    return map


def update_map(map_id, map_name, resource_path):
    ''' update map record
        if map_id no exists, raise MAP_ERROR
    '''
    map = get_map(map_id)
    if map:
        if map_name:
            map.map_name = map_name 
        if resource_path:
            map.resource_path = resource_path
        db.session.add(map)
        db.session.commit()
        return map
    else:
        raise InvalidModelUsage('update map fail, %d no exists!' % map_id, MAP_ERROR)


def delete_map(map_id):
    ''' delete map record
        if map_id no exists, raise MAP_ERROR
    '''
    map = get_map(map_id) 
    if map:
        db.session.delete(map)
        db.session.commit()
    else:
        raise InvalidModelUsage('delete map fail, %d no exists!' % map_id, MAP_ERROR)


def get_all_map():
    ''' query all map records
    '''
    maps = Map.query.all()
    return maps


def get_adjacent_maps(longitude, latitude, distance=10):
    """Return adjacent maps."""
    adjacent_maps = []
    for m in get_all_maps():
        lon = m.longitude
        lat = m.latitude
        dis = haversine(longitude, latitude, lon, lat)
        if dis <= distance:
            adjacet_maps.append(m)
    return adjacent_maps
