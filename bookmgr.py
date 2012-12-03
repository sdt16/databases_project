from sqlalchemy import create_engine
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash, current_app
from controller import Controller
from models import app
from flask_login_user import DbUser
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed

controller = Controller()

login_manager = LoginManager()
login_manager.init_app(app)

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

@login_manager.user_loader
def load_user(user_id):
    user = controller.query_user(int(user_id))
    if user:
        return DbUser(user)
    else:
        return None


@app.route('/login', methods=["POST"])
def login():
    user = controller.login_user(request.form['email'], request.form['pass'])
    if user is not None:
        login_user(DbUser(user))
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    else:
        #TODO: Error page
        pass
    return redirect(url_for('book_mgr'))

@app.route('/book_mgr')
@login_required
def book_mgr():
    return render_template('book_mgr.html', page_title='Book Manager')

@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
