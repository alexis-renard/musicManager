from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import get_sample, get_author, Author, User
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Tiny Amazon",
	books=get_sample()
	)

class AuthorForm(Form):
	id		= HiddenField('id')
	name	= StringField('Nom', validators=[DataRequired()])

@app.route("/edit/author/")
@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id=None):
	if id is not None:
		a = get_author(id)
	else:
		a = Author(name="")
		db.session.add(a)
		db.session.commit()
		id = a.id
	f = AuthorForm(id=id, name=a.name)
	return render_template("edit-author.html", author=a, form=f)

@app.route("/author/<int:id>")
def one_author(id):
	a = get_author(id)
	livres = a.books
	return render_template(
		"home.html",
		title="Little Amazon",
		books=livres
	)

@app.route("/save/author/", methods=("POST",))
def save_author():
	a = None
	f = AuthorForm()
	if f.validate_on_submit():
		id = int(f.id.data)
		a = get_author(id)
		a.name = f.name.data
		db.session.commit()
		return redirect(url_for('one_author', id=a.id))
	a = get_author(int(f.id.data))
	return render_template("edit-author.html", author=a, form=f)

class LoginForm(Form):
	username = StringField('Username')
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

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('home'))
