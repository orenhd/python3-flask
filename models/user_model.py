from mongoengine import Document, StringField, ListField, ObjectIdField

import config


class UserModel(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    friends = ListField(StringField())
    meta = {
        'collection': config.databases['mongodb']['usersCollection'],
        'strict': False
    }
