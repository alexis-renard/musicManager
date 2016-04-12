from .app import db, login_manager
from flask.ext.login import UserMixin
from wtforms import Form, StringField
from wtforms.validators import DataRequired

import sys #sys correspond à la version de python, si la version est inférieur à python3
#on importera whooshalchemy qui gère les searchbar avec les versions antérieur à python3
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy

#Création de la table belong entre album et Genre
belong = db.Table('belong',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'genre_id')
)

#Création de la table Artist
class Artist(db.Model):
    __searchable__ = ['name']

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))

#many to many avec genre ? Comme ça on pourrait récupérer tous les artists d'un genre
#ça implique que l'on doit creer une secondary table également

    def __repr__(self):
        return "<Artist (%d) %s>" % (self.id, self.name)

    def get_id_a(self):
        return self.id

    def get_name(self):
        return self.name

    def get_compositor(self):
        return self.compositor

#Création de la table Genre
class Genre(db.Model):
    __searchable__ = ['name_g']

    id           = db.Column(db.Integer, primary_key=True)
    name_g       = db.Column(db.String(100))

    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.name_g)

    def get_id_g(self):
        return self.id

    def get_name_g(self):
        return self.name_g


#Création de la table Ablum
class Album(db.Model):
    __searchable__ = ['title','releaseYear','compositor']

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100))
    releaseYear = db.Column(db.String(100))
    img         = db.Column(db.String(100))
    compositor  = db.Column(db.String(100))
    artist_id   = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artists      = db.relationship("Artist", backref = db.backref("albums", lazy="dynamic"))
    genres       = db.relationship("Genre", secondary=belong, backref = db.backref("albums", lazy="dynamic"))

    def __repr__(self):
        return "<Album (%d) %s>" % (self.id, self.title)

    def get_id_al(self):
        return self.id

    def get_title(self):
        return self.title

    def get_releaseYear(self):
        return self.releaseYear

    def get_img(self):
        return self.img

    def get_artist_id(self):
        return self.artist_id

#Création de la table User
class User(db.Model, UserMixin):
    username    = db.Column(db.String(50), primary_key=True)
    password    = db.Column(db.String(64))

    def get_id(self):
        return self.username

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
    classe = StringField('classe', validators=[DataRequired()])

def get_artist(id):
    return Artist.query.get(id)

def get_album(id):
    return Album.query.get(id)

def get_genre(id):
    return Album.query.get(id)

def get_albums_artist(idartist):
    return Album.query.filter(Album.artist_id==idartist).all()

def get_albums_genre(idgenre):
    #return Album.query.filter(Album.genres.contains(get_genre(idgenre))).all()
    #return Genre.query.filter(Genre.id=).all()
    #return Genre.query.filter(Album.genres.any(id=idgenre))
    return Genre.albums

def get_artists_genre(idgenre):
    return Artist.query.filter(Album.genres.any(id=idgenre)).all()

def get_genre(name_g):
    return Genre.query.get(name_g)

def get_sample_albums():
    return Album.query.limit(5).all()

def get_sample_genre():
    return Genre.query.limit(5).all()

def get_sample_artists():
    return Artist.query.limit(5).all()

def get_date_albums(releaseY):
    return Album.query.filter(Album.releaseYear==releaseY).all()

if enable_search:
    whooshalchemy.whoosh_index(app, Artist)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
