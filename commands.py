from .app import manager, db

@manager.command
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    #creation de toutes les tables
    db.create_all()

    #chargement de notre jeu de données
    import yaml
    albums = yaml.load(open(filename))

    #import des modèles
    from .models import Artist, Album, Genre, get_genre

    #creation de tous les auteurs
    artists = {}
    for b in albums:
        a = b["by"]
        if a not in artists:
            o = Artist(name=a)
            db.session.add(o)
            artists[a] = o
    db.session.commit()

    #creation de tous les genres
    genres=set()
    for b in albums:
        liste_genre = b["genre"]
        for g in liste_genre:
            if g not in genres:
                o = Genre(name_g=g)
                db.session.add(o)
                genres.add(g)
    db.session.commit()

    #creation de tous les albums
    for b in albums:
        a = artists[b["by"]]
        o = Album(id            = b["entryId"],
                  title         = b["title"],
                  releaseYear   = b["releaseYear"],
                  img           = b["img"],
                  compositor    = b["parent"],
                  artist_id     = a.id,
        )
        genres = b["genre"]
        for genre in genres:
            g= Genre(name_g=genre)
            o.genre.append(g)
        db.session.add(o)
    db.session.commit()

@manager.command
def syncdb():
    ''' Creates all missing tables. '''
    db.create_all()

@manager.command
def newuser(username, password):
    '''Adds a new user.'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()

@manager.command
def passwd(username,password):
    from .models import load_user
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = load_user(username)
    u.password = m.hexdigest()
    db.session.commit()
