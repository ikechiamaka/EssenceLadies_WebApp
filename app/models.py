from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Check if user is admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    stats = db.Column(db.String(10), nullable=False)
    dress_size = db.Column(db.String(10), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    eye_color = db.Column(db.String(20), nullable=False)
    service_level = db.Column(db.String(20), nullable=False)
    languages = db.Column(db.String(100), nullable=False)
    bisexual = db.Column(db.Boolean, default=False)
    incall_location = db.Column(db.String(100), nullable=True)
    outcall_location = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('profiles', lazy=True))
    tonight = db.Column(db.Boolean, default=False)  # Indicates if profile is featured in "Escorts Tonight"

    def __repr__(self):
        return f"Profile('{self.name}', '{self.nationality}', '{self.age}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    escort_name = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    time_to_call = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    length_of_booking = db.Column(db.String(20), nullable=False)
    date_of_booking = db.Column(db.Date, nullable=False)
    additional_details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Booking('{self.escort_name}', '{self.date_of_booking}')"
