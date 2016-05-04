from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os.path

app = Flask(__name__)
app.debug = True

manager = Manager(app)

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

app.config['BOOTSTRAP_SERVE_LOCAL']=True
Bootstrap(app)

app.config ['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "7b31fdc6-85ff-4855-9e25-7dbbe134d746"

login_manager = LoginManager(app)

login_manager.login_view = "login"
