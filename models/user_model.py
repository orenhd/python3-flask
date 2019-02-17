from mongoengine import Document, StringField, ListField

import config


class User(Document):

    username = StringField(required=True)
    password = StringField(required=True)
    friends = ListField(StringField())  # TODO: define an accurate model
    meta = {
        'collection': config.databases['mongodb']['usersCollection'],
        'strict': False
    }
