import os

from mongoengine import connect


def connect_db():
    connection_params = {
        "username": os.environ.get('MONGODB_USER', 'root'),
        "password": os.environ.get('MONGODB_PASS', 'moomoomoo'),
        "authentication_source": os.environ.get('MONGODB_AUTHDB', 'admin'),
        "host": os.environ.get('MONGODB_HOST', '127.0.0.0.1'),
        "port": int(os.environ.get('MONGODB_PORT', 27017))
    }
    return connect(os.environ.get('MONGODB_NAME'), **connection_params)
