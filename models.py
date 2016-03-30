from .app import db, login_manager
from flask.ext.login import UserMixin

#Création de la table belong entre album et Genre
belong = db.Table('belong',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'genre_id')
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

    def get_compositor(self):
        return self.compositor

#Création de la table Genre
class Genre(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name_g       = db.Column(db.String(100))

    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.nom_g)

    def get_id_g(self):
        return self.id

    def get_nom_g(self):
        return self.nom_g


#Création de la table Ablum
class Album(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100))
    releaseYear = db.Column(db.String(100))
    img         = db.Column(db.String(100))
    compositor  = db.Column(db.String(100))
    artist_id   = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artist      = db.relationship("Artist", backref = db.backref("album", lazy="dynamic"))
    genre       = db.relationship("Genre", secondary=belong, backref = db.backref("album", lazy="dynamic"))

    def __repr__(self):
        return "<Album (%d) %s>" % (self.id, self.title)

    def get_id_al(id_al):
        return self.id

    def get_title(title):
        return self.title

    def get_releaseYear(self):
        return self.releaseYear

    def get_img(self):
        return self.img

#Création de la table User
class User(db.Model, UserMixin):
    username    = db.Column(db.String(50), primary_key=True)
    password    = db.Column(db.String(64))

    def get_id(self):
        return self.username

#Création des getters
def get_artist(id):
    return Artist.query.get(id)

def get_album(id):
    return Album.query.get(id)

def get_albums_artist(idartist):
    return Album.query.filter(Album.artist_id==idartist).all()

def get_genre(name_g):
    return Genre.query.get(name_g)

def get_sample():
    return Album.query.limit(5).all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
