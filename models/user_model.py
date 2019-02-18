from mongoengine import Document, StringField, ListField, ObjectIdField

import config


class UserModel(Document):
    id = ObjectIdField(required=True, db_field='_id.$oid', primary_key=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    friends = ListField(StringField())
    meta = {
        'collection': config.databases['mongodb']['usersCollection'],
        'strict': False
    }
