WTF_CSRF_ENABLED = True
SECRET_KEY = "boop"

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
		'id': 'eyed'
		'secret': 'scoop'
	},
	'google': {
		'id': 'asdf'
		'secret': 'scoopdiwoop'
	}
}

if os.environ.get('DATABASE_URL') is None:
	CELERY_BROKER_URL = 'redis://localhost:6379'
	CELERY_BACKEND = 'redis://localhost:6379'
else:
	CELERY_BROKER_URL = os.environ['REDIS_URL']
	CELERY_BACKEND = os.environ['REDIS_URL']

# How long rooms will live for, measured in seconds
ROOM_TTL = 1500

# Optionally prevent users from querying database directly
# by using a buffer variable
AVOID_ROOM_DATABASE_QUERIES = False
AVAILABLE_ROOMS = []
