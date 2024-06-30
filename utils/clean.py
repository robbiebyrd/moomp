import logging

from utils.db import connect_db
from utils.types import OBJECT_TYPES

logger = logging.getLogger(__name__)


def clean():
    connect_db()

    for object_type in OBJECT_TYPES:
        object_type.objects().delete()
