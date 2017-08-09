from app import db
from flask_login import UserMixin

UserRoom = db.Table('UserRoom',
	db.Column('id', db.Integer, primary_key=True),
	db.Column('userId', db.Integer, db.ForeignKey('users.id')),
	db.Column('roomId', db.Integer, db.ForeignKey('rooms.id')),
	db.Column('creationTime', db.DateTime))

class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	social_id = db.Column(db.String(128), nullable=False, unique=True)
	nickname = db.Column(db.String(128), nullable=False, unique=True)
	email = db.Column(db.String(256), nullable=True)
	about_me = db.Column(db.String(256), nullable=True)
	profile_picture_url = db.Column(db.String(256), nullable=True)
	
	last_room_password = db.Column(db.String(64), nullable=True)

	auth_provider = db.Column(db.String(256), nullable=False)
	total_time_online = db.Column(db.DateTime, nullable=True)
	approved_rooms = db.relationship('Room', secondary = UserRoom, backref='User', lazy='dynamic')

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname

	def __repr__(self):
		return '<User %r>' % (self.nickname)

	def profile_picture(self, size):
		if self.auth_provider == 'google':
			return self.profile_picture_url + "?sz=%s" % size
		elif self.auth_provider == 'facebook':
			return self.profile_picture_url + '?width=%s&height=%s' % (size, size)

class Room(db.Model, UserMixin):
	__tablename__ = 'rooms'
	id = db.Column(db.Integer, primary_key=True)
	roomname = db.Column(db.String(64), nullable=False, unique=True)
	created_time = db.Column(db.DateTime, nullable=False)
	password = db.Column(db.String(64), nullable=False)
	approved_users = db.relationship('User', secondary = UserRoom, backref='Room', lazy='dynamic')
	#active_users = db.relationship('User', secondary = UserRoom, backref='Room', lazy='dynamic')

	def __repr__(self):
		return '<Room %r>' % (self.roomname)


	'''
	users can be in either, both, or neither of two possible states:

	- in_room: user is currently in 'room/roomname'

	- is_approved: user is allowed to be in 'room/roomname'

	users who are not approved cannot be in a room (thus users in room must be approved)
	'''
	
	'''
	def enter_room(self, user):
		if not self.in_room(user):
			self.active_users.append(user)
			return self

	def exit_room(self, user):
		if self.in_room(user):
			self.active_users.remove(user)
			return self

	def in_room(self, user):
		return self.active_users.filter(UserRoom.c.userId == user.id).count() > 0
	'''
	
	def approve_user(self, user):
		if not self.is_approved(user):
			self.approved_users.append(user)
			return self

	def disapprove_user(self, user):
		if self.is_approved(user):
			self.approved_users.remove(user)
			return self

	def is_approved(self, user):
		return self.approved_users.filter(UserRoom.c.userId == user.id).count() > 0