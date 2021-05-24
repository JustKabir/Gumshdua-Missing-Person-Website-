from datetime import datetime
from gumshuda import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(25), nullable = False)
	email = db.Column(db.String(), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	post = db.relationship('AddMissingPerson', backref = 'user', lazy=True)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}')"

class AddMissingPerson(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(25), nullable = False)
	age = db.Column(db.Integer(), nullable=False)
	height = db.Column(db.Integer(), nullable=False)
	colour = db.Column(db.String(10), nullable = False)
	lostAt = db.Column(db.String(255), nullable=False)
	reward = db.Column(db.Integer(), default= 0,)
	gender = db.Column(db.String(), nullable=False)
	contactNo = db.Column(db.Integer(), nullable=False)
	image = db.Column(db.String(20), nullable = False, default='default.jpg')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	attire = db.Column(db.String(100), nullable=False)
	country = db.Column(db.String(20), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f"User('{self.name}', '{self.age}')"


