from indoor_position import db
from indoor_position.models.map import get_map
from indoor_position.common.error_handler import *

# adjacent beacons table
adjacent_beacon_table = db.Table('adjacent_beacon', db.Model.metadata,
        db.Column('from_beacon_id', db.Integer, db.ForeignKey('beacons.beacon_id')),
        db.Column('to_beacon_id', db.Integer, db.ForeignKey('beacons.beacon_id'))
        )
 
class Beacon(db.Model):
    __tablename__ = 'beacons'
    beacon_id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.Integer)
    minor = db.Column(db.Integer)

    # beacon's adjacent relation
    to_beacons = db.relationship('Beacon',
            secondary=adjacent_beacon_table,
            primaryjoin=(adjacent_beacon_table.c.from_beacon_id == beacon_id),
            secondaryjoin=(adjacent_beacon_table.c.to_beacon_id == beacon_id),
            backref=db.backref('from_beacons', lazy='dynamic'),
            lazy='dynamic')
    
    # infomation in a map
    map_id = db.Column(db.Integer, db.ForeignKey('maps.map_id'))
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float) 
    location_z = db.Column(db.Float)

    def __init__(self, beacon_id, major, minor, map, location_x, location_y, location_z):
        self.beacon_id = beacon_id
        self.major = major
        self.minor = minor
        self.map = map
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = location_z

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_adjacent_beacons(self):
        return self.to_beacons.all()


def get_beacon(beacon_id):
    beacon = Beacon.query.filter_by(beacon_id=beacon_id).first()
    return beacon


def create_beacon(beacon_id, major, minor, map_id, location_x, location_y, location_z):
    map = get_map(map_id)
    if map is None:
        raise InvalidModelUsage("create beacon fail, map[%d] no exists!" % map_id, MAP_ERROR)

    beacon = get_beacon(beacon_id)
    if beacon:
        raise InvalidModelUsage("create beacon fail, beacon[%d] exists!" % beacon_id, BEACON_ERROR)
    beacon = Beacon(beacon_id, major, minor, map, location_x, location_y, location_z)
    beacon.save()
    return beacon


def update_beacon(beacon_id, major, minor, map_id, x, y, z):
    beacon = Beacon.query.filter_by(beacon_id=beacon_id).first()
    if beacon:
        if major:
            beacon.major = major
        if minor:
            beacon.minor = minor
        if map_id:
            map = get_map(map_id)
            if map:
                beacon.map = map
            else:
                raise InvalidModelUsage('update beacon fail, map[%d] no exists!' % map_id, MAP_ERROR)
        if x:
            beacon.location_x = x
        if y:
            beacon.location_y = y
        if z:
            beacon.location_z = z
        beacon.save()
        return beacon
    else:
        raise InvalidModelUsage('update beacon fail, beacon[%d] no exists!' % beacon_id, BEACON_ERROR)


def delete_beacon(beacon_id):
    beacon = get_beacon(beacon_id)
    if beacon:
        db.session.delete(beacon)
        db.session.commit()
        return beacon
    else:
        raise InvalidModelUsage('delete beacon fail, %d no exists!' % beacon_id, BEACON_ERROR)


def get_all_beacons():
    beacons = Beacon.query.all()
    return beacons


def add_adjacent_beacons(beacon_id1, beacon_id2):
    beacon1 = get_beacon(beacon_id1)
    beacon2 = get_beacon(beacon_id2)
    if beacon1 and beacon2:
        beacon1.to_beacons.append(beacon2)
        beacon1.from_beacons.append(beacon2)
    else:
        if not beacon1:
            raise InvalidModelUsage('add adjacent beacons fail, %d no exists!' % beacon_id1, BEACON_ERROR)
        if not beacon2:
            raise InvalidModelUsage('add adjacent beacons fail, %d no exists!' % beacon_id2, BEACON_ERROR)


def get_adjacent_beacons(beacon_id):
    beacon = get_beacon(beacon_id)
    if beacon:
        return beacon.get_adjacent_beacons()
    else:
        raise InvalidModelUsage('get adjacent beacons fail, %d no exists!' % beacon_id, BEACON_ERROR)
