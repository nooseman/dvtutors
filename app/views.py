from flask import redirect, url_for, render_template, flash, g, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, models, db, celery
from app.models import User, Room, UserRoom
from app.oauth import OAuthSignIn
from .forms import RoomForm, EditForm
from datetime import datetime
from .tasks import remove_room

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html',
							title='Home',
							user=g.user)

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('Unable to find %s.' % nickname, 'danger')
		return redirect(url_for('home'))
	return render_template('user.html',
							user=user)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Changes have been saved.', 'success')
		return redirect(url_for('user'), nickname=g.user.nickname)
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.errorhandler(401)
def unauthorized_error(error):
	return render_template('401.html'), 401
	
@app.route('/login')
def login():
	return render_template('login.html',
							title='Login',
							user=g.user)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
	form = RoomForm()
	if form.validate_on_submit():
		db.session.add(g.user)
		
		#create a list of all existing rooms with this roomname
		room = Room.query.filter_by(roomname=form.roomname.data).first()

		# the room doesn't exist yet, so make it and set its name
		# and password to the given data
		if room == None:
			room = Room(roomname=form.roomname.data,
						password=form.roomkey.data,
						created_time=datetime.utcnow())

			#delete room in 25 min
			remove_room.apply_async(args=[room.roomname], countdown=1500)	

			db.session.add(room)
		#the room does exist
		else:
			#if the 'attempted' password isn't the same as the room's password
			if room.password != form.roomkey.data:
				flash('That password\'s not right.', 'danger')
				return redirect(url_for('chat'))
		
		room.approve_user(g.user)
		db.session.commit()
		return redirect(url_for('room', roomname=form.roomname.data))
	return render_template('chat.html',
							title='Chat',
							form=form)

@app.route('/list')
@login_required
def list():
	if app.config['AVOID_ROOM_DATABASE_QUERIES']:
		rooms = app.config['AVAILABLE_ROOMS']
	else:
		rooms = Room.query.all()

	ages = []

	for room in rooms:
		tdelta = datetime.utcnow() - room.created_time
		ages.append(tdelta.seconds // 60)
	
	#return render_template('list.html', rooms=rooms, ages=ages)
	return render_template('list.html', room_age=zip(rooms, ages))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/room/<roomname>')
@login_required
def room(roomname):
	room = Room.query.filter_by(roomname=roomname).first()
	if room == None:
		flash('A room called %s doesn\'t exist yet. You can make it here, if you\'d like.' % roomname, 'info')
		return redirect(url_for('chat'))

	if room.is_approved(g.user) or room.password == "":
		return render_template('room.html',
								title='Chat',
								roomname=roomname)
	else:
		flash('You\'re not approved to join %s yet.' % roomname, 'info')
		return redirect(url_for('chat'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('home'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('home'))
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email, auth_provider, profile_picture_url = oauth.callback()
	if social_id is None:
		flash('Authentication failed.', 'danger')
		return redirect(url_for('home'))
	user = User.query.filter_by(social_id=social_id).first()
	if not user:
		nickname = User.make_unique_nickname(username)
		user = User(social_id=social_id, nickname=nickname, email=email, auth_provider=auth_provider, profile_picture_url=profile_picture_url)
		db.session.add(user)
		db.session.commit()
	login_user(user, True)
	return redirect(url_for('home'))