from flask import Flask, render_template, session, redirect, url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'
boostrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
Migrate = Migrate(app, db)


# 使用重定向保存数据到cooike中
@app.route('/', methods=['GET', 'POST'])
def index():
	 form = NameForm()
	 if form.validate_on_submit():
	 	old_name = session.get('name')
	 	if old_name is not None and old_name != form.name.data:
	 		flash('Looks like you have change your name!')
	 	session['name'] = form.name.data
	 	return redirect(url_for('index'))
	 return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role)

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')
	def __repr__(self):
		return '<Role %r>' % self.name


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<Role %r>' % self.username