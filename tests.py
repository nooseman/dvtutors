#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

'''
TODO:

- add test_setup_room, test_connect_room, etc

'''

class SimpleTestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_profile_picture(self):
		pass

	def test_make_unique_nickname(self):
		u = User(id='1', nickname='john', social_id='1', auth_provider='google')
		db.session.add(u)
		db.session.commit()

		nickname = User.make_unique_nickname('john')
		assert nickname != 'john'

		u = User(id='2', nickname=nickname, social_id='2', auth_provider='facebook')
		db.session.add(u)
		db.session.commit()

		nickname2 = User.make_unique_nickname('john')
		assert nickname2 != 'john'
		assert nickname2 != nickname

if __name__ == '__main__':
	unittest.main()