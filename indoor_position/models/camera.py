# coding=UTF-8
from indoor_position import db
from indoor_position.models.map import *
from indoor_position.common.error_handler import *

class Camera(db.Model):
    __tablename__ = 'cameras'
    camera_id = db.Column(db.Integer)
    camera_name = db.Column(db.Text)
    map_id = db.Column(db.Integer, db.ForeignKey('maps.map_id'))
    car_license = db.Column(db.Text)						          #车牌号
    car_channel = db.Column(db.Integer)						#通道号
    car_port = db.Column(db.Integer, primary_key=True)							#车位号
    port_stauts = db.Column(db.Integer)						#车位状态
    find_time = db.Column(db.Integer)						          #报警时间戳
 
    def __init__(self,camera_id=None,camera_name=None,map_id=None,car_license=None,car_channel=None,car_port=None,port_stauts=None,find_time=None):
    	self.camera_id = camera_id
    	self.camera_name = camera_name
    	self.map_id = map_id
    	self.car_license = car_license
    	self.car_channel = car_channel
    	self.car_port = car_port
    	self.port_stauts = port_stauts
    	self.find_time = find_time

    def save(self):
    	db.session.add(self)
    	db.session.commit()
    	return self

def get_camera(car_port):
    camera = Camera.query.filter_by(car_port=car_port).first()
    return camera  

def create_camera(camera_id, camera_name,map_id,car_license,car_channel,car_port,port_stauts,find_time):				                                    #*************************					
    map = get_map(map_id)
    if map is None:
        raise InvalidModelUsage("create camera fail, map[%d] no exists!" % map_id, MAP_ERROR)

    camera = get_camera(car_port)
    if camera is not None:
        raise InvalidModelUsage('create camera fail, car_port %d exists!' % car_port, CAMERA_ERROR)

    camera = Camera(camera_id, camera_name,map_id,car_license,car_channel,car_port,port_stauts,find_time)                                                                          #************************
    db.session.add(camera)
    db.session.commit()
    return camera

def update_camera(camera_id, camera_name,map_id,car_license,car_channel,car_port,port_stauts,find_time):
    ''' update camera record
        if camera_id no exists, raise CAMERA_ERROR
    '''
    camera = get_camera(car_port)
    if camera:
        if map_id:
            camera.map_id = map_id 
        else:
                raise InvalidModelUsage('update beacon fail, map[%d] no exists!' % map_id, MAP_ERROR)
        if camera_name:
            camera.camera_name = camera_name
        if car_license:
            camera.car_license = car_license
        if car_channel:
            camera.car_channel = car_channel
        if car_port:
            camera.car_port = car_port
        if port_stauts:
            camera.port_stauts = port_stauts
        if find_time:
            camera.find_time = find_time
        db.session.add(camera)
        db.session.commit()
        return camera
    else:
        raise InvalidModelUsage('update camera fail, car_port %d no exists!' % car_port, CAMERA_ERROR)

def delete_camera(car_port):
    ''' delete camera record
        if camera_id no exists, raise CAMERA_ERROR
    '''
    camera = get_camera(car_port) 
    if camera:
        db.session.delete(camera)
        db.session.commit()
    else:
        raise InvalidModelUsage('delete camera fail, car_port %d no exists!' % car_port, CAMERA_ERROR)

def get_all_camera():
    ''' query all camera records
    '''
    cameras = Camera.query.all()
    return cameras










