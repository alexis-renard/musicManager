from .app import manager, db

@manager.command
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    #creation de toutes les tables
    db.create_all()

    #chargement de notre jeu de données
    import yaml
    books = yaml.load(open(filename))

    #import des modèles
    from .models import Author, Book

    #premiere pass : creation de tous les auteurs
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    #deuxieme pass : creation de tous les livres
    for b in books:
        a = authors[b["author"]]
        o = Book(price      = b["price"],
                 title      = b["title"],
                 url        = b["url"]  ,
                 img        = b["img"]  ,
                 author_id  = a.id)
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
