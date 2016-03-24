from .app import db, login_manager
from flask.ext.login import UserMixin

class Artist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
    compositor  = db.Column(db.String(100))

    def __repr__(self):
        return "<Artist (%d) %s>" % (self.id, self.name)

    def get_id_a(self):
        return self.id

    def get_name(self):
        return self.name

    def get_compositor(self):
        return self.compositor

class Album(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.Float)
    releaseYear = db.Column(db.String(100))
    img         = db.Column(db.String(100))
    artist_id   = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artist      = db.relationship("Artist", backref = db.backref("albums", lazy="dynamic"))

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

class Genre(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    nom_g       = db.Column(db.String(100))

    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.nom_g)

    def get_id_g(self):
        return self.id

    def get_nom_g(self):
        return self.nom_g

class User(db.Model, UserMixin):
    username    = db.Column(db.String(50), primary_key=True)
    password    = db.Column(db.String(64))

    def get_id(self):
        return self.username

def get_artist(id):
    return Artist.query.get(id)

def get_album(id):
    return Album.query.get(id)

def get_genre(id):
    return Genre.query.get(id)

def get_sample():
    return Album.query.limit(100).all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
