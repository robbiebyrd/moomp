import logging

from utils.db import connect_db

logger = logging.getLogger(__name__)


def check():
    a = connect_db()
    print(a)
