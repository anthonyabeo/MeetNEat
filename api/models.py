from datetime import datetime

from flask_login import UserMixin

from MeetNEat import db


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    about_me = db.Column(db.String(1000), nullable=True)
    password = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))

    def __str__(self):
        return self.username


class Request(db.Model):

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    meal_type = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    meal_time = db.Column(db.Time)
    filled = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime(), index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Proposal(db.Model):

    __tablename__ = 'proposals'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_proposed_to = db.Column(db.String, nullable=False)
    user_proposed_from = db.Column(db.String, nullable=False)
    filled = db.Column(db.Boolean, default=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))


class MealDate(db.Model):

    __tablename__ = 'meal_dates'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_1 = db.Column()
    user_2 = db.Column()
    restaurant_name = db.Column(db.String, nullable=False)
    restaurant_address = db.Column(db.String, nullable=False)
    restaurant_picture = db.Column(db.BLOB)
    meal_time = db.Column(db.Time)

