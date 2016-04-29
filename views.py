from .app import app, db
from flask import render_template, url_for, redirect, request, g
from datetime import datetime
from .models import User, Artist, Album, Genre, Compositor, Playlist, get_artist, get_album, get_sample_albums
from .models import get_sample_artists, get_albums_artist, get_albums_genre, get_sample_genre, get_genre
from .models import get_artists_genre, get_date_albums, SearchForm, ArtistForm,get_artist_search, get_genre_search
from .models import get_album_search_title, get_compositor_search, get_album_search_releaseYear, get_all_artist
from .models import get_all_albums, get_all_genre, GenreForm, AlbumForm
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, PasswordField, validators
from wtforms.validators import DataRequired, Required, EqualTo, Length
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required
import copy #Importation de copy pour gérer les pointeurs lors de la suppression d'albums

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

@app.route('/search/<query>')
@login_required
def search_results(query):
#def search_results(classe,query=None):
    album_results_title = get_album_search_title(query)
    album_results_releaseYear = get_album_search_releaseYear(query)
    artist_results = get_artist_search(query)
    genre_results = get_genre_search(query)
    album_result = [album_results_title, album_results_releaseYear]
    compositor_results = get_compositor_search(query)
    return render_template(
			'search.html',
	    	query		                = query,
            artist_results              = artist_results,
            genre_results               = genre_results,
            album_result                = album_result,
            compositor_results          = compositor_results
	)

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Musique / Playlist",
	albums=get_sample_albums()
	)

@app.route("/album/")
@app.route("/album/<int:id>")
def one_album(id=None):
	if id is not None:
		a = get_album(id)
		id_artist=a.get_artist_id()
		artist=get_artist(id_artist)
		artist_name=artist.get_name()
		#artist = get_artist(a.get_artist_id()).get_name()
		title = a.get_title()
		return render_template(
			"album.html",
			title=title,
			album=a,
			artist=artist_name
		)
	else:
		return render_template(
			"albums.html",
			title="Albums Sample",
			albums=get_all_albums()
		)

@app.route("/edit/album/")
@app.route("/edit/album/<int:id>")
@login_required
def edit_album(id=None):
	if id is not None:
		a = get_album(id)
	else:
		a = Album(title="")
		db.session.add(a)
		db.session.commit()
		id = a.id
	f = AlbumForm(id=id, title=a.title, releaseYear=a.releaseYear)
	return render_template("edit-album.html", album=a, form=f)

@app.route("/save/album/", methods=("POST",))
def save_album():
    a = None
    f = AlbumForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_album(id)
        if f.title.data != "":
            a.title = f.title.data
        if f.releaseYear.data !="":
            a.releaseYear = f.releaseYear.data
        db.session.commit()
        return redirect(url_for('one_album', id=a.id))
    a = get_album(int(f.id.data))
    return render_template("edit-album.html", album=a, form=f)

@app.route("/delete/album/")
@app.route("/delete/album/<int:id>")
@login_required
def delete_album(id):
    if id == None:
        return redirect(url_for('one_album'))
    else:
        a = get_album(id)
        artist = get_artist(a.get_artist_id())
        genres = a.get_genres()
        db.session.delete(a)
        i = 0
        for album in artist.albums:
            i+=1
        if i == 0:
            db.session.delete(artist)
        for genre in genres :
            j = 0
            for album in genre.albums:
                j+=1
            if j == 0:
                db.session.delete(genre)
        db.session.commit()
    return redirect(url_for('one_album'))

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
			title="All Artists",
			artists=get_all_artist()
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
			genres=get_all_genre()
		)

@app.route("/edit/genre/")
@app.route("/edit/genre/<int:id>")
@login_required
def edit_genre(id=None):
	if id is not None:
		a = get_genre(id)
	else:
		a = Genre(name_g="")
		db.session.add(a)
		db.session.commit()
		id = a.id
	f = GenreForm(id=id, name_g=a.name_g)
	return render_template("edit-genre.html", genre=a, form=f)

@app.route("/save/genre/", methods=("POST",))
def save_genre():
	a = None
	f = GenreForm()
	if f.validate_on_submit():
		id = int(f.id.data)
		a = get_genre(id)
		a.name_g = f.name_g.data
		db.session.commit()
		return redirect(url_for('one_genre', id=a.id))
	a = get_genre(int(f.id.data))
	return render_template("edit-genre.html", genre=a, form=f)

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
