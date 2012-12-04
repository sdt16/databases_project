from models import db, User, Book, Series, Person, Authors, Illustrators, Editors, Contributors, Translators

list_attrs = {'authors': Authors,'illustrators': Illustrators, 'editors': Editors,
              'contributors': Contributors, 'translators': Translators}

class Controller():

    def create_user(self, name, email, password, vendor_code):
        user = User(name, "", email, password, vendor_code)
        db.session.add(user)
        db.session.commit()
    def login_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if (user.password == password):
            return user
        else:
            return None
    def query_user(self, user_id):
            return User.query.get(user_id)

    def get_books_for_vendor(self, vendor_code, num, offset):
        books = Book.query.filter_by(vendor_code = vendor_code)
        return books

    def get_book_by_id(self, vendor_code, id):
        book = Book.query.filter_by(vendor_code = vendor_code, id=id).first()
        return book

    def update_book(self, book_id, attr, value):
        if attr not in list_attrs.keys():
            Book.query.filter_by(id=book_id).update({attr: value})
        else:
            list_attrs[attr].query.filter_by(book_id=book_id).delete()
            for v in value:
                obj = list_attrs[attr](book_id, v)
                db.session.add(obj)
        db.session.commit()

    def get_selected_people(self, book_id):
        return_dict = dict()
        for k,v in list_attrs.items():
            people = v.query.filter_by(book_id = book_id).all()
            list = map(lambda person_obj: person_obj.person_id, people)
            return_dict[k] = list
        return return_dict

    def get_all_series(self):
        return Series.query

    def get_people(self):
        return Person.query