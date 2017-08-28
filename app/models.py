from app import db
from flask_login import UserMixin
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username',db.String(80), unique=True)
    email = db.Column('email',db.String(120), unique=True)
    password = db.Column('password' ,db.String(250))
    registered_on = db.Column('registered_on' ,db.DateTime)
    admin = db.Column('admin',db.Boolean)
    devices = db.relationship('Device' , backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)


class Device(db.Model):
	__tablename__ = 'devices'
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	devicename = db.Column('devicename',db.String(50),unique=True)
	devicerol = db.Column('devicerol',db.String(20))
	deviceso = db.Column('deviceso',db.String(20))
	devicesshv2 = db.Column('devicesshv2',db.String(10))
	deviceip= db.Column('deviceip',db.String(20))
	deviceuserlogin = db.Column('deviceuserlogin',db.String(20))
	devicepassword = db.Column('devicepassword',db.String(250))
	devicepasswordena = db.Column('devicepasswordena',db.String(250))
	devicesnmp=db.Column('devicesnmp',db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	deviceconfigs = db.relationship('DeviceConfig' , backref='device',lazy='dynamic')


	def __init__(self,devicename,devicerol,deviceso,devicesshv2,deviceip,deviceuserlogin,devicepassword,devicepasswordena,devicesnmp):
		self.devicename=devicename
		self.devicerol=devicerol
		self.deviceso=deviceso
		self.devicesshv2=devicesshv2
		self.deviceip=deviceip
		self.deviceuserlogin=deviceuserlogin
		self.devicepassword=devicepassword
		self.devicepasswordena=devicepasswordena
		self.devicesnmp=devicesnmp

	def __repr__(self):
		desc = self.devicename + '-'+ self.devicerol
		return '<Device %r>' % (desc)



class DeviceConfig(db.Model):
	__tablename__ = 'deviceconfigs'
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	deviceconfig = db.Column('deviceconfig',db.String(300))
	devicecurrentconfig = db.Column('devicecurrentconfig',db.String(300))
	saved_on = db.Column('save_on' ,db.DateTime)
	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))

	def __init__(self,deviceconfig,devicecurrentconfig):
		self.deviceconfig=deviceconfig
		self.devicecurrentconfig=devicecurrentconfig
		self.saved_on=datetime.datetime.now()
