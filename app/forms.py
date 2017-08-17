from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User
import profanityfilter

class EditForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

	
	def validate(self):
		if not Form.validate(self):
			return False
		if self.nickname.data == self.original_nickname:
			return True
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user != None:
			self.nickname.errors.append('This name is taken. Try again.')
			return False
		return True

class RoomForm(Form):
	roomname = StringField('roomname', validators=[DataRequired()])
	roomkey = StringField('roomkey', validators=[Length(min=0, max=20)])

	def validate(self):
		if not Form.validate(self):
			return False
		if profanityfilter.is_profane(self.roomname.data):
			self.roomname.errors.append('This room name is not allowed. Try again.')
			return False
		return True