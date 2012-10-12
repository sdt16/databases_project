from sqlalchemy import create_engine
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash


#configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DATABASE = 'postgresql://devo:test@localhost:5432/bookmgr_test'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('BOOKMGR_SETTINGS', silent=True)

def connect_db():
	return create_engine(app.config['DATABASE'])

@app.route('/')
def home():
	return render_template('index.html', page_title='Home')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
