from models import db, User

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