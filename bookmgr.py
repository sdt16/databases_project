from series_edit_form import edit_series
from sqlalchemy import create_engine
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash, current_app
from controller import Controller
from models import app
from flask_login_user import DbUser
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user, confirm_login
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, identity_loaded, UserNeed, RoleNeed
from book_edit_form import book_edit_form
from person_edit_form import person_form
import os

controller = Controller()

login_manager = LoginManager()
login_manager.init_app(app)

def connect_db():
    return create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('book_mgr'))
    return render_template('index.html', page_title='Home', not_logged_in=True)

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

@app.route('/add_book', methods=["GET", "POST"])
@login_required
def book_add():
    people = controller.get_people()
    people_selected = controller.get_selected_people()
    form = book_edit_form(**people_selected)
    form.series.choices = [(series.id, series.title) for series in controller.get_all_series()]
    people_list = [(person.id, (person.last_name + ", " + person.first_name)) for person in people]
    form.authors.choices = people_list
    form.illustrators.choices = people_list
    form.editors.choices = people_list
    form.contributors.choices = people_list
    form.translators.choices = people_list
    if form.validate_on_submit():
        controller.new_book(current_user.get_vendor_code(), form.data)
        flash("Successfully created a new book")
        return redirect(url_for('book_mgr'))
    return render_template('book_edit.html', page_title='Add a new book', book = controller.new_book(), form = form)

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
        for k,v in form.data.items():
            if v is not None:
                controller.update_book(book_id, k, v)
        flash('Successfully updated')
        return redirect(url_for('book_mgr'))
    return render_template('book_edit.html', page_title='Edit a book', book=book, form=form)

@app.route('/view_series')
@login_required
def view_series():
    series = controller.get_all_series()
    return render_template('view_series.html', series=series)

@app.route('/edit_series/<int:series_id>', methods=["GET", "POST"])
@login_required
def series_edit(series_id):
    series = controller.get_series_by_id(series_id)
    form = edit_series(title = series.title, begin_date = series.begin_date, end_date = series.end_date)
    if form.validate_on_submit():
        for k,v in form.data.items():
            if v is not None:
                controller.update_series(series_id, k, v)
        flash('Successfully updated')
        return redirect(url_for('view_series'))

    return render_template('series_edit.html', page_title='Series Edit', series=series, form=form)

@app.route('/edit_person/<int:person_id>', methods=["GET", "POST"])
@login_required
def person_edit(person_id):
    person = controller.get_person_by_id(person_id)
    form = person_form(first_name = person.first_name, last_name = person.last_name, birthday = person.birthday)
    if form.validate_on_submit():
        for k,v in form.data.items():
            if v is not None:
                controller.update_person(person_id, k, v)
        flash('Successfully updated')
        return redirect(url_for('view_people'))
    return render_template('person_edit.html', page_title='People Edit', person=person, form=form)

@app.route('/add_person', methods=["GET", "POST"])
@login_required
def person_add():
    form = person_form()
    if form.validate_on_submit():
        controller.add_person(form.data)
        flash('Successfully added a new person')
        return redirect(url_for('view_people'))
    return render_template('person_edit.html', page_title='People Edit', form=form)

@app.route('/view_people')
@login_required
def view_people():
    people = controller.get_people()
    return render_template('view_people.html', people=people)

@app.route('/add_series', methods=["GET", "POST"])
@login_required
def series_add():
    form = edit_series()
    if form.validate_on_submit():
        controller.add_series(form.data)
        flash('Successfully added a series')
        return redirect(url_for('view_series'))
    return render_template('series_edit.html', page_title='Series Edit', form=form)


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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
