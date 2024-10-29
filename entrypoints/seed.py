import json

from models.account import Account
from models.character import Character
from models.instance import Instance
from models.object import Object
from models.portal import Portal
from models.room import Room
from services.authn import AuthNService


class Seeder:

    def __init__(self, file):
        with open(file, 'r') as f:
            self._content = json.load(open(file))

    def seed(self):
        if instances := self._content.get('instances'):
            self.seed_instances(instances)
        if accounts := self._content.get('accounts'):
            self.seed_accounts(accounts)
        if characters := self._content.get('characters'):
            self.seed_characters(characters)
        if rooms := self._content.get('rooms'):
            self.seed_rooms(rooms)
        if portals := self._content.get('portals'):
            self.seed_portals(portals)

    @staticmethod
    def hydrate(obj, model_type, field):
        model_types = {
            "instance": [Instance, 'name'],
            "account": [Account, 'email'],
            "character": [Character, 'name'],
            "room": [Room, 'name'],
            "object": [Object, 'name'],
            "portal": [Portal, 'name']
        }

        if model_types[model_type] is not None and obj.get(field) and isinstance(obj[field], str):
            query = {model_types[model_type][1]: obj.get(field)}
            obj[field] = model_types[model_type][0].objects(**query).first()
        return obj

    def seed_instances(self, instances):
        for instance in instances:
            if not Instance.objects(name=instance.get("name")):
                instance = self.hydrate(instance, 'instance', 'parent')
                Instance(**instance).save()

    def seed_accounts(self, accounts):
        for account in accounts:
            if not Account.objects(email=account.get("email")):
                account = self.hydrate(account, 'instance', 'instance')
                account['password'] = AuthNService.encrypt_password(account.get("password"))
                Account(**account).save()

    def seed_characters(self, characters):
        for character in characters:
            if not Character.objects(name=character.get("name")):
                character = self.hydrate(character, 'account', 'account')
                Character(**character).save()

    def seed_rooms(self, rooms):
        for room in rooms:
            if not Room.objects(name=room.get("name")):
                room = self.hydrate(room, 'character', 'owner')
                room = self.hydrate(room, 'room', 'parent')
                Room(**room).save()

    def seed_objects(self, objects):
        for obj in objects:
            if not Object.objects(name=obj.get("name")):
                obj = self.hydrate(obj, 'character', 'owner')
                obj = self.hydrate(obj, 'object', 'parent')
                obj = self.hydrate(obj, 'character', 'holder')
                obj = self.hydrate(obj, 'room', 'room')
                Object(**obj).save()

    def seed_portals(self, portals):
        for portal in portals:
            portal = self.hydrate(portal, 'room', 'to_room')
            portal = self.hydrate(portal, 'room', 'from_room')
            portal = self.hydrate(portal, 'character', 'owner')

            if not Portal.objects(
                    name=portal.get("name"),
                    from_room=portal.get('from_room'),
                    to_room=portal.get('to_room')
            ):
                Portal(**portal).save()
