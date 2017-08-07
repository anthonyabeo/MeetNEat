from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from mongoengine import connect, Document, StringField, FloatField, EmailField, DateTimeField, BooleanField, \
                        ReferenceField, ImageField
from werkzeug.security import check_password_hash, generate_password_hash

connect('meetneat', host='localhost', port=27017)


class User(Document):
    username = StringField(required=True, max_lenght=64, unique=True)
    first_name = StringField(max_length=64)
    last_name = StringField(max_length=64)
    email = EmailField(unique=True, null=True)
    about_me = StringField(max_length=1000)
    password_hash = StringField(max_length=100)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def confirm_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.objects.get(id=data['id'])
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.username


class Request(Document):
    meal_type = StringField(max_length=64, required=True)
    location_string = StringField(max_length=64)
    longitude = FloatField(min_value=0.00)
    latitude = FloatField(min_value=0.00)
    meal_time = StringField(max_length=64)
    created = DateTimeField(default=datetime.now())
    modified = DateTimeField(default=datetime.now())
    filled = BooleanField(default=False)
    user = ReferenceField(User)


class Proposal(Document):
    proposal_host = ReferenceField(User)
    proposal_guest = ReferenceField(User)
    filled = BooleanField(default=False)
    request = ReferenceField(Request)


class MealDate(Document):
    proposal = ReferenceField(Proposal)
    restaurant_name = StringField(max_length=64)
    restaurant_address = StringField(max_length=64)
    #restaurant_picture = ImageField()
    meal_time = DateTimeField()
