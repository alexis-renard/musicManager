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
    from .models import Artist, Album

    #premiere pass : creation de tous les auteurs
    artists = {}
    for b in artists:
        a = b["artists"]
        if a not in artists:
            o = Artist(name=a)
            db.session.add(o)
            artists[a] = o
    db.session.commit()

    #deuxieme pass : creation de tous les livres
    for b in artists:
        a = artists[b["artists"]]
        o = Album(title         = b["price"],
                  releaseYear   = b["title"],
                  img           = b["img"],
                  artist_id     = a.id)
        db.session.add(o)
    db.session.commit()

    # #troisième pass : creation de tous les genres
    # for b in albums:


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
