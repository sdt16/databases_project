from sqlalchemy import create_engine
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash, current_app
from controller import Controller
from models import app
from flask_login_user import DbUser
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, identity_loaded, UserNeed, RoleNeed
from book_edit_form import book_edit_form
from decimal import *

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
    books = controller.get_books_for_vendor(current_user.get_vendor_code(), 20, 0)
    return render_template('book_mgr.html', page_title='Book Manager', books=books)

@app.route('/edit_book/<int:book_id>', methods=["GET", "POST"])
@login_required
def book_edit(book_id):
    book = controller.get_book_by_id(current_user.get_vendor_code(), book_id)
    people = controller.get_people()
    people_selected = controller.get_selected_people(book_id)
    form = book_edit_form(territory = book.territory, currency = book.currency, series = book.series, **people_selected)
    form.series.choices = [(series.id, series.title) for series in controller.get_all_series()]
    people_list = [(person.id, (person.last_name + ", " + person.first_name)) for person in people]
    form.authors.choices = people_list
    form.illustrators.choices = people_list
    form.editors.choices = people_list
    form.contributors.choices = people_list
    form.translators.choices = people_list
    if form.validate_on_submit():
        flash('Success')
        for k,v in form.data.items():
            if v is not None:
                controller.update_book(book_id, k, v)
        return redirect(url_for('book_mgr'))
    return render_template('book_edit.html', page_title='Edit a book', book=book, form=form)

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


@login_manager.user_loader
def load_user(user_id):
    user = controller.query_user(int(user_id))
    if user:
        return DbUser(user)
    else:
        return None

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    identity.provides.add(UserNeed(current_user.get_vendor_code()))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
