from functools import partial
from operator import is_not

from models.account import Account
from models.character import Character
from models.instance import Instance
from models.object import Object
from models.portal import Portal
from models.room import Room
from models.script import Script, ScriptType, ScriptTypes
from services.authn import AuthNService


def description():
    return "Seed the database."


def run():
    instance_data = {
        'name': 'Hereville',
        'description': 'Hereville: A village that is here',
        'properties': {
            "msg_connect": 'You are connected to ${instance.name}.'
        }
    }

    if not Instance.objects(name=instance_data.get("name")):
        Instance(**instance_data).save()

    instance = Instance.objects(name=instance_data.get("name")).first()

    account_array = [
        {
            "email": "wizard@yourhost.com",
            "password": AuthNService.encrypt_password("wizard"),
            "instance": instance
        },
        {
            "email": "programmer@yourhost.com",
            "password": AuthNService.encrypt_password("programmer"),
            "instance": instance
        },
    ]

    account_instances = list(
        filter(
            partial(is_not, None),
            [None if Account.objects(email=data.get("email")) else Account(**data) for data in account_array],
        )
    )

    if account_instances:
        Account.objects.insert(account_instances, load_bulk=False)

    character_array = [
        {
            "name": "Wizard",
            "display": "The Wizard",
            "visible": True,
            "account": Account.objects(email="wizard@yourhost.com").first(),
        },
        {
            "name": "Architect",
            "display": "The Architect",
            "visible": True,
            "account": Account.objects(email="wizard@yourhost.com").first(),
        },
        {
            "name": "Builder",
            "display": "The Builder",
            "visible": True,
            "account": Account.objects(email="wizard@yourhost.com").first(),
        },
        {
            "name": "Programmer",
            "display": "The Programmer",
            "visible": True,
            "account": Account.objects(email="programmer@yourhost.com").first(),
        },
    ]

    character_instances = list(
        filter(
            partial(is_not, None),
            [Character(**data) if not Character.objects(name=data.get("name")) else None for data in character_array],
        )
    )

    if len(character_instances) > 0:
        Character.objects.insert(character_instances, load_bulk=False)

    the_prog = Character.objects(name="Programmer").first()
    the_wiz = Character.objects(name="Wizard").first()
    the_builder = Character.objects(name="Builder").first()
    the_architect = Character.objects(name="Architect").first()

    room_array = [
        {
            "owner": the_wiz,
            "name": "Nowhere",
            "description": "A nondescript void. It looks like Nowhere",
            "visible": False,
        },
        {
            "owner": the_wiz,
            "name": "Lobby",
            "description": "A building lobby. It is incredibly bare and generic looking.",
            "visible": True,
        },
    ]

    room_instances = list(
        filter(
            partial(is_not, None),
            [Room(**data) if not Room.objects(name=data.get("name"), owner=the_wiz) else None for data in room_array],
        )
    )

    if len(room_instances) > 0:
        Room.objects.insert(room_instances, load_bulk=False)

    nowhere = Room.objects(name="Nowhere").first()
    lobby = Room.objects(name="Lobby").first()

    if not Portal.objects(from_room=lobby, to_room=nowhere, name="Ethereal Portal"):
        Portal.objects.create(
            owner=the_wiz,
            from_room=lobby,
            to_room=nowhere,
            name="Ethereal Portal",
            alias_to=["n"],
            alias_from=["s"],
            description_from="A glowing portal",
            description_to="A tiny window looking into a building's lobby.",
            visible=True,
            reversible=True,
        )
    if not Object.objects(name="Atom", owner=the_wiz):
        Object.objects.create(
            owner=the_wiz,
            name="Atom",
            description="An atom of a mysterious put powerful element.",
            visible=False,
            holder=the_wiz,
            properties={"locked": True},
        )

    if not Object.objects(name="An Apple", owner=the_wiz):
        Object.objects.create(
            owner=the_wiz,
            name="An Apple",
            holder=the_wiz,
            parent=Object.objects(name="Atom").first(),
            description="A delicious, McIntosh Red apple.",
            visible=True,
            properties={"locked": True},
        )

    the_wiz.room = nowhere
    the_prog.room = lobby
    the_builder.room = lobby
    the_architect.room = lobby

    the_wiz.save()
    the_prog.save()
    the_builder.save()
    the_architect.save()

    Script.objects.update_one(
        owner=the_wiz,
        name='test_script',
        scripts=[ScriptType(
            type=ScriptTypes.Character,
            script='''function(character, inventory, room, nearby, account, exits)
            return character, inventory, room, nearby, account, exits
        end'''
        )],
        attached=[the_wiz, the_prog, the_builder, the_architect]
    )
