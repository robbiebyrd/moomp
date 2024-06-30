import os

from mongoengine import connect


def connect_db():
    connection_params = {
        "username": os.environ.get('MONGODB_USER'),
        "password": os.environ.get('MONGODB_PASS'),
        "authentication_source": os.environ.get('MONGODB_AUTHDB'),
        "host": os.environ.get('MONGODB_HOST'),
        "port": int(os.environ.get('MONGODB_PORT'))
    }
    return connect(os.environ.get('MONGODB_NAME'), **connection_params)
