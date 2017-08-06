from flask_mongoengine import Document
from mongoengine import StringField


class Admin(Document):
    username = StringField()