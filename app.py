from flask import Flask

app = Flask(__name__)
app.debug = True

from flask.ext.script import Manager
manager = Manager(app)

app.config['BOOTSTRAP_SERVE_LOCAL']=True
from flask.ext.bootstrap import Bootstrap
Bootstrap(app)

import os.path
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

from flask.ext.sqlalchemy import SQLAlchemy
app.config ['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "7b31fdc6-85ff-4855-9e25-7dbbe134d746"

from flask.ext.login import LoginManager
login_manager = LoginManager(app)

login_manager.login_view = "login"
