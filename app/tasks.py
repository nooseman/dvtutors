from flask import redirect, url_for, flash
from app import app, celery, db, models

@celery.task()
def remove_room(roomname):
	room = models.Room.query.filter_by(roomname=roomname)
	room.approved_users = []

	users = models.User.query.filter_by(room in approved_rooms).all()
	for user in users:
		user.approved_rooms.remove(room)

	models.Room.query.filter_by(roomname=roomname).delete()
	db.session.commit()

	return 'Room ' + roomname + ' deleted.'