from models.character import Character
from models.room import Room
from utils.db import connect_db


def seed():
    connect_db()

    character_array = []
    room_array = []

    if not Character.objects(name='Wizard'):
        character_array.append({
            'name': 'Wizard',
            'email': 'wizard@localhost',
            'password': 'w1z4rd',
            'display': 'The Wizard',
            'visible': True
        })

    if not Character.objects(name='Programmer'):
        character_array.append({
            'name': 'Programmer',
            'email': 'programmer@localhost',
            'password': 'Pr09R4mmEr',
            'display': 'The Programmer',
            'visible': True
        })

    character_instances = [Character(**data) for data in character_array]

    if character_instances:
        Character.objects.insert(character_instances, load_bulk=False)

    the_prog = Character.objects(name='Programmer').first()
    the_wiz = Character.objects(name='Wizard').first()

    if not Room.objects(name='Nowhere'):
        room_array.append({
            'owner': the_wiz,
            'name': 'Nowhere',
            'description': 'A nondescript void.',
            'visible': False
        })

    if not Room.objects(name='Lobby'):
        room_array.append({
            'owner': the_wiz,
            'name': 'Lobby',
            'description': 'A building lobby. It is incredibly bare and generic looking.',
            'visible': True
        })

    room_instances = [Room(**data) for data in room_array]

    if room_instances:
        Room.objects.insert(room_instances, load_bulk=False)

    nowhere = Room.objects(name='Nowhere').first()
    lobby = Room.objects(name='Lobby').first()

    the_wiz.room = nowhere
    the_prog.room = lobby
    the_wiz.save()
    the_prog.save()
