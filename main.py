from models.character import CharacterCreateDTO, CharacterUpdateDTO
from utils.db import connect_db
from seed import seed
from services.character import CharacterService


def main():
    seed()
    #
    # cs.rename( "RobbieByrdNew")
    # cs.update_property( {"a": "1"})
    # a = CharacterService.get_by_username('RobbieByrdNew')
    # print(cs.where())

if __name__ == "__main__":
    main()

# from pymongo import MongoClient
# from rich import print
# import enum
# from templates import get_room
# from bson.objectid import ObjectId
# from pprint import pprint
# from mongoengine import connect
#
# from models.character import Character
# from models.object import Object
# from models.portal import Portal
# from models.room import Room

# class PortalDirection(enum.Enum):
#     FROM = '_from'
#     TO = '_to'
#
#
# client = MongoClient('mongodb://root:moomoomoo@localhost:27017/')
# collection = client['moo']
#
#
# def get_character(username):
#     return collection['characters_flat'].find_one({"name": username})
#
#
# def get_portal_commands(character):
#     this_room = get_current_room(character)
#
#     portal_commands = []
#
#     for x in this_room['exits']:
#         portal_commands = portal_commands + x['aliasTo'] + [x['name']]
#         return {x['_id']: portal_commands}
#
# def move_character(character, direction):
#     for ext in character['room']['exits']:
#         if direction in ext['aliasTo'] or direction == ext['name']:
#             collection['characters'].update_one({'_id': character['_id']}, {"$set": {'_roomId': ext['_to']}})
#
#
# def warp_character(character, portal, direction: PortalDirection = PortalDirection.TO):
#     collection['characters'].update_one({'_id': character['_id']}, {"$set": {'_roomId': portal[direction.value]}})
#
#
# def get_current_room(character):
#     return character['room']
#
#
# warp_character(get_character('wizard'), {"_to": ObjectId("665df6e75f0326791e311cef")})
# print(get_room(get_current_room(get_character('wizard'))))
# move_character(get_character('wizard'), "Black Hole")
# print(get_room(get_current_room(get_character('wizard'))))
# # print(get_portal_commands(get_character('wizard')))
# move_character(get_character('wizard'), "out")
# print(get_room(get_current_room(get_character('wizard'))))
# # print(get_portal_commands(get_character('wizard')))
# move_character(get_character('wizard'), "out")
# print(get_room(get_current_room(get_character('wizard'))))
#
#

connect_db()

# ch = Character()
# ch.name = 'a'
# ch.email = '<EMAIL>'
# ch.password = 'asd'
# ch.display = 'display'
# ch.visible = True
# ch.room = Room(name="asd")
# ch.room.owner = Character(name='b', email='b', password='b', display='b').save()
# ch.room.save()
#
# ch.save()
#
# for ch in Character.objects().select_related(max_depth=10):
#     pprint(ch.to_json())
# for rm in Room.objects():
#     pprint(rm.to_json())
# pprint(Character.objects())
# print(Room.objects())
# print(Object.objects())
# print(Portal.objects())
