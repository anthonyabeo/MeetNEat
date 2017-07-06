from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from MeetNEat import db, login_manager


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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Request.query.all()

    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()


class Proposal(db.Model):

    __tablename__ = 'proposals'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_proposed_to = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user_proposed_from = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    filled = db.Column(db.Boolean, default=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Proposal.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MealDate(db.Model):

    __tablename__ = 'meal_dates'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_1 = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user_2 = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    restaurant_name = db.Column(db.String(128), nullable=False)
    restaurant_address = db.Column(db.String(128), nullable=False)
    restaurant_picture = db.Column(db.BLOB)
    meal_time = db.Column(db.Time)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return MealDate.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

