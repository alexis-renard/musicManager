from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import User, Artist, Album, get_artist, get_album, get_sample, get_all_albums
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, PasswordField, validators
from wtforms.validators import DataRequired, Required, EqualTo, Length
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Le sith de l'amour <3",
	albums=get_sample()
	)

class ArtistForm(Form):
	id			= HiddenField('id')
	name		= StringField('Nom', validators=[DataRequired()])
	compositor  = StringField('Compositeur')

@app.route("/albums/")
def albums():
	return render_template(
	"albums.html",
	title="Albums List",
	albums=get_sample()
	)

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
	name = a.name
	return render_template(
		"home.html",
		title="Le sith de l'amour <3",
		albums="salut",#a ajouter la query qui nous donne tous les albums qu'a fait l'artiste
		name=name
	)

@app.route("/save/artist/", methods=("POST",))
def save_artist():
	a = None
	f = ArtistForm()
	if f.validate_on_submit():
		id = int(f.id.data)
		a = get_artist(id)
		a.name = f.name.data
		db.session.commit()
		return redirect(url_for('one_artist', id=a.id))
	a = get_artist(int(f.id.data))
	return render_template("edit-artist.html", artist=a, form=f)

class LoginForm(Form):
	username = StringField('Username') #ce qui est entre simple quote correspond au label du champs
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


class RegisterForm(Form):
	username = StringField('Username')
	password = PasswordField('Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4)
	])
	confirm = PasswordField('Repeat Password')
	next = HiddenField() #à quoi sert exactement le next ?

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

@app.route("/register/", methods=("GET","POST",))
def register():
	f = RegisterForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		m = sha256()
		m.update(f.password.data.encode())
		u = User(username=f.username.data, password=m.hexdigest())
		db.session.add(u)
		db.session.commit()
		login_user(u)
		next = f.next.data or url_for("home")
		return redirect(next)
	return render_template("register.html",form = f)

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('home'))
