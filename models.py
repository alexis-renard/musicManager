from .app import db, login_manager, app
from flask.ext.login import UserMixin
from wtforms import StringField, HiddenField, PasswordField, validators
from wtforms.validators import DataRequired
from flask.ext.wtf import Form

#Création de la table belong entre album et Genre
belong = db.Table('belong',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'genre_id')
)

belong_playlist_album = db.Table('belong_playlist_album',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'playlist_id')
)

#Création de la table Artist
class Artist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))

    def __repr__(self):
        return "<Artist (%d) %s>" % (self.id, self.name)

    def get_id_a(self):
        return self.id

    def get_name(self):
        return self.name


#Création de la table Genre
class Genre(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name_g       = db.Column(db.String(100))

    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.name_g)

    def get_id_g(self):
        return self.id

    def get_name_g(self):
        return self.name_g

class Compositor(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class Playlist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
    user_name   = db.Column(db.Integer, db.ForeignKey("user.username"))
    user        = db.relationship("User", backref = db.backref("playlists", lazy="dynamic"))
    albums      = db.relationship("Album", secondary=belong_playlist_album, backref = db.backref("playlists", lazy="dynamic"))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


#Création de la table Ablum
class Album(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(100))
    releaseYear     = db.Column(db.String(100))
    img             = db.Column(db.String(100))
    compositor_id   = db.Column(db.Integer, db.ForeignKey("compositor.id"))
    artist_id       = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artist          = db.relationship("Artist", backref = db.backref("albums", lazy="dynamic"))
    genres          = db.relationship("Genre", secondary=belong, backref = db.backref("albums", lazy="dynamic"))

    def __repr__(self):
        return "<Album (%d) %s>" % (self.id, self.title)

    def get_id_al(self):
        return self.id

    def get_title(self):
        return self.title

    def get_compositor(self):
        return self.compositor_id

    def get_releaseYear(self):
        return self.releaseYear

    def get_img(self):
        return self.img

    def get_artist_id(self):
        return self.artist_id

    def get_genres(self):
        return self.genres

#Création de la table User
class User(db.Model, UserMixin):
    username        = db.Column(db.String(50), primary_key=True)
    password        = db.Column(db.String(64))

    def get_id(self):
        return self.username


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


class ArtistForm(Form):
	id			= HiddenField('id')
	name		= StringField('Nom', validators=[DataRequired()])

class GenreForm(Form):
	id			= HiddenField('id')
	name_g		= StringField('Nom Genre', validators=[DataRequired()])

class AlbumForm(Form):
    id			= HiddenField('id')
    title		= StringField('Titre Album')
    releaseYear	= StringField('Année de sortie')

def get_all_artist():
    return Artist.query.all()

def get_all_albums():
    return Album.query.all()

def get_all_genre():
    return Genre.query.all()

def get_artist(id):
    return Artist.query.get(id)

def get_album(id):
    return Album.query.get(id)

def get_genre(id):
    return Genre.query.get(id)

def get_albums_artist(idartist):
    return Album.query.filter(Album.artist_id==idartist).all()

def get_albums_genre(idgenre):
    return Genre.albums

def get_artists_genre(idgenre):
    return Artist.query.filter(Album.genres.any(id=idgenre)).all()

def get_genre(name_g):
    return Genre.query.get(name_g)

def get_compositor(id):
    return Compositor.query.get(id)

def get_sample_albums():
    return Album.query.limit(5).all()

def get_sample_genre():
    return Genre.query.limit(3).all()

def get_sample_artists():
    return Artist.query.limit(5).all()

def get_artist_search(search):
    return Artist.query.filter(Artist.name.like("%"+search+"%")).all()

def get_album_search_title(search):
    return Album.query.filter(Album.title.like("%"+search+"%")).all()

def get_compositor_search(search):
    return Compositor.query.filter(Compositor.name.like("%"+search+"%")).all()

def get_album_search_releaseYear(search):
    return Album.query.filter(Album.releaseYear.like("%"+search+"%")).all()

def get_genre_search(search):
    return Genre.query.filter(Genre.name_g==search).all()

def get_date_albums(releaseY):
    return Album.query.filter(Album.releaseYear==releaseY).all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

@app.context_processor
def utility_processor():
    def get_name_compositor_context(idcompositor):
        return get_compositor(idcompositor).get_name()
    def get_name_artist_context(idartist):
        return get_artist(idartist).get_name()
    return dict(get_name_compositor_context=get_name_compositor_context,get_name_artist_context=get_name_artist_context)
