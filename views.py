from .app import app, db, MAX_SEARCH_RESULTS
from flask import render_template, url_for, redirect, request, g
from datetime import datetime
from .models import User, Artist, Album, get_artist, get_album, get_sample_albums, get_sample_artists, get_albums_artist, get_albums_genre, get_sample_genre, get_genre, get_artists_genre, get_date_albums, SearchForm
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, PasswordField, validators
from wtforms.validators import DataRequired, Required, EqualTo, Length
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('home'))
    return redirect(url_for('search_results', query=g.search_form.search.data))
#	return redirect(url_for('search_results', query=g.search_form.search.data, classe=g.search_form.classe.data))

@app.route('/search/<query>')
@login_required
def search_results(query):
#def search_results(classe,query=None):
    results = classe.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template(
			'search.html',
	    	query		= query,
	    	results		= results
	)


@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Musique / Playlist",
	albums=get_sample_albums()
	)

class ArtistForm(Form):
	id			= HiddenField('id')
	name		= StringField('Nom', validators=[DataRequired()])
	compositor  = StringField('Compositeur')

@app.route("/albums/")
@app.route("/albums/<int:id>")
def one_album(id=None):
	if id is not None:
		a = get_album(id)
		title = a.get_title()
		return render_template(
			"album.html",
			title=title,
			album=a
		)
	else:
		return render_template(
			"albums.html",
			title="Albums Sample",
			albums=get_sample_albums()
		)

@app.route("/date/")
@app.route("/date/<int:releaseY>")
def one_date(releaseY):
	return render_template(
	"date.html",
	title="Release Year",
	albums=get_date_albums(releaseY)
	)


@app.route("/artist/")
@app.route("/artist/<int:id>")
def one_artist(id=None):
	if id is not None:
		a = get_artist(id)
		name = a.get_name()
		return render_template(
			"artist.html",
			title=name,
			albums=get_albums_artist(id)
		)
	else:
		return render_template(
			"artists.html",
			title="Artists Sample",
			artists=get_sample_artists()
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

@app.route("/test_api")
def api():
	g=get_genre(1)
	return

@app.route("/genre/")
@app.route("/genre/<int:id>")
def one_genre(id=None):
	if id is not None:
		g = get_genre(id)
		name_g = g.get_name_g()
		return render_template(
			"genre.html",
			title=name_g,
			genre=g,
			artists=get_artists_genre(id)
		)
	else:
		return render_template(
			"genres.html",
			title="Genre Sample",
			genres=get_sample_genre()
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
