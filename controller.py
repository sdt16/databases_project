from models import db, User

class Controller():
	def create_user(self, name, email, password, vendor_code):
		user = User(name, "", email, password, vendor_code)
		db.session.add(user)
		db.session.commit()
	def login_user(self, email, password):
		user = User.query.filter_by(email=email).first()
		return dict(user_id=user.id)