from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Artist, Album, Genre, get_artist, get_album, get_genre, get_sample
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Le site de l'amour <3",
	albums=get_sample()
	)

class ArtistForm(Form):
	id			= HiddenField('id')
	name		= StringField('Nom', validators=[DataRequired()])
	compositor  = StringField('Compositeur')

@app.route("/edit/artist/")
@app.route("/edit/artist/<int:id>")
@login_required
def edit_artist(id=None):
	if id is not None:
		a = get_artist(id)
	else:
		a = Artist(name="")
		db.session.add(a)
		db.session.commit()
		id = a.id
	f = ArtistForm(id=id, name=a.name)
	return render_template("edit-artist.html", artist=a, form=f)

@app.route("/artist/<int:id>")
def one_artist(id):
	a = get_artist(id)
	albums = a.albums
	return render_template(
		"home.html",
		title="Le site de l'amour <3",
		albums=albums
	)

@app.route("/save/artist/", methods=("POST",))
def save_author():
	a = None
	f = ArtistForm()
	if f.validate_on_submit():
		id = int(f.id.data)
		a = get_artist(id)
		a.name = f.name.data
		db.session.commit()
		return redirect(url_for('one_artist', id=a.id))
	a = get_artist(int(f.id.data))
	return render_template("edit-artist.html", author=a, form=f)

class LoginForm(Form):
	username = StringField('Username')
	password = PasswordField('Password')
	next = HiddenField()

	def get_authenticated_user(self):
		user = User.query.get(self.username.data)
		if user is None:
			return None
		m = sha256()
		m.update(self.password.data.encode())
		passwd = m.hexdigest()
		return user if passwd == user.password else None

@app.route("/login/", methods=("GET","POST",))
def login():
	f = LoginForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("login.html",form = f)

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('home'))
