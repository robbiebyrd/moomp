from models.account import Account
from models.character import Character
from models.instance import Instance
from models.object import Object
from models.portal import Portal
from models.room import Room
from models.speech import Speech

OBJECT_TYPES = [Account, Instance, Character, Object, Portal, Room]
SCRIPT_OBJECT_TYPES = [Character, Object, Portal, Room, Speech]
