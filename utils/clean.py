import logging

from models.account import Account
from models.character import Character
from models.events import Event
from models.instance import Instance
from models.object import Object
from models.portal import Portal
from models.room import Room
from models.script import Script
from models.speech import Speech
from utils.db import connect_db

logger = logging.getLogger(__name__)
ALL_OBJECT_TYPES = [
    Account,
    Character,
    Event,
    Instance,
    Object,
    Portal,
    Room,
    Script,
    Speech,
]


def clean():
    connect_db()

    for object_type in ALL_OBJECT_TYPES:
        object_type.objects().delete()
