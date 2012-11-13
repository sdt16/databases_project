from sqlalchemy import create_engine
from flask import request, session, g, redirect, url_for, \
	abort, render_template, flash
from controller import Controller
from models import app

controller = Controller()

def connect_db():
	return create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def home():
	return render_template('index.html', page_title='Home')

@app.route('/user', methods=["POST"])
# warning, this is obviously a really dumb way of storing user creds,
# with plain text passwords and such.
def create_user():
	controller.create_user(request.form['name'],
		request.form['email'], request.form['pass'],
		request.form['vendor_code'])
	return "success"

@app.route('/login', methods=["POST"])
def login():
	user = controller.login_user(request.form['email'], request.form['pass'])
	return str(user["user_id"])


if __name__ == '__main__':
	app.run(host='0.0.0.0')
