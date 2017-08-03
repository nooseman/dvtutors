from app import app, celery, db, models

@celery.task()
def remove_room(roomname):
	models.Room.query.filter_by(roomname=roomname).delete()
	db.session.commit()
	
	return 'Room ' + roomname + ' deleted.'