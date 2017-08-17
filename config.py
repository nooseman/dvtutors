WTF_CSRF_ENABLED = True
SECRET_KEY = "Ya/g+!y3/s>~D[d)S67U4Ew/IiDaq+"

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#location of database file
if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#location of folder for storing migration files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False

OAUTH_CREDENTIALS = {
	'facebook': {
		'id': '1703552289947767',
		'secret': '709adbe160b1e033b437d84aed7d633b'
	},
	'google': {
		'id': '977228534153-8odev575d1qj301ebj0l01fe4jgk2t7a.apps.googleusercontent.com',
		'secret': 'TxaIZ7riMFbVI5wxJP-ZiCBS'
	}
}

if os.environ.get('DATABASE_URL') is None:
	CELERY_BROKER_URL = 'redis://localhost:6379'
	CELERY_BACKEND = 'redis://localhost:6379'
else:
	CELERY_BROKER_URL = os.environ['REDIS_URL']
	CELERY_BACKEND = os.environ['REDIS_URL']


# Optionally prevent users from querying database directly
# by using a buffer variable
AVOID_ROOM_DATABASE_QUERIES = False
AVAILABLE_ROOMS = []