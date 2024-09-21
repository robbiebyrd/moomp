from models.account import Account
from models.character import Character
from models.object import Object
from models.portal import Portal
from models.room import Room
from models.speech import Speech

OBJECT_TYPES = [Account, Character, Object, Portal, Room]
SCRIPT_OBJECT_TYPES = OBJECT_TYPES + [Speech]
