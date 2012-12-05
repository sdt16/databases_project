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

    def get_series_by_id(self, series_id):
        return Series.query.filter_by(id = series_id).first()

    def get_selected_people(self, book_id=None):
        return_dict = dict()
        for k,v in list_attrs.items():
            if book_id:
                people = v.query.filter_by(book_id = book_id).all()
                list = map(lambda person_obj: person_obj.person_id, people)
                return_dict[k] = list
            else:
                return_dict[k] = []
        return return_dict

    def update_series(self, series_id, attr, value):
        Series.query.filter_by(id=series_id).update({attr: value})
        db.session.commit()

    def get_all_series(self):
        return Series.query

    def get_people(self):
        return Person.query

    def new_book(self):
        return Book()

    def new_book(self, vendor_code=None, book_info=None):
        if vendor_code and book_info:
            book = Book(vendor_code, book_info['title'], book_info['imprint'], book_info['eisbn'], book_info['pisbn'],
                book_info['language'], book_info['list_price'], book_info['currency'], book_info['release_date'],
                book_info['publishing_date'], book_info['description'], book_info['bisac'], book_info['bic'],
                book_info['territory'], book_info['adult'], book_info['edition'], book_info['series'], book_info['volume'])
            db.session.add(book)
            db.session.commit()
        else:
            return Book()


