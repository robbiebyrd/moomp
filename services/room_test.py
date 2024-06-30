from pprint import pprint

from models.portal import PortalUpdateDTO, Portal
from models.room import RoomCreateDTO, RoomUpdateDTO
from services.character import CharacterService
from services.character_test import create_test_character, cleanup_test_character
from services.portal import PortalService
from services.room import RoomService
from utils.db import connect_db

connect_db()


def cleanup_test_room(room_name: str):
    room = RoomService.get_by_name(room_name)
    if room:
        RoomService.remove(room.id)
    cleanup_test_character(room_name + ' User')


def create_test_room(room_name: str):
    cleanup_test_room(room_name)
    create_test_character(room_name + ' User')
    char = CharacterService.get_by_username(room_name + ' User')
    room = RoomCreateDTO(
        name=room_name,
        description=room_name + ' Room',
        owner=str(char.id),
        visible=True,
        parent_id=''
    )
    RoomService.create(room)


def test_create_room():
    create_test_room('Test Room')

    cs = RoomService.get_by_name('Test Room')

    assert cs.name == 'Test Room'
    assert cs.description == 'Test Room Room'
    assert cs.visible is True

    cleanup_test_room('Test Room')


def test_rename_room():
    create_test_room('Test Room')

    csi = RoomService.new(RoomService.get_by_name('Test Room'))
    csi.rename('Test Room Renamed')
    csn = RoomService.get_by_name('Test Room Renamed')

    assert csn.name == 'Test Room Renamed'

    cleanup_test_room('Test Room Renamed')


def test_update_room():
    create_test_room('Test Room')

    csi = RoomService.get_by_name('Test Room')
    csu = RoomService.new(csi.id)

    csu.update(
        room=RoomUpdateDTO(
            name="Test Room 2",
            description="Test Room 2",
        )
    )
    cs = RoomService.get_by_name('Test Room 2')

    assert cs.name == 'Test Room 2'
    assert cs.description == 'Test Room 2'

    cleanup_test_room('Test Room 2')


def test_update_room_properties():
    create_test_room('Test Room with Properties')

    rs = RoomService(RoomService.get_by_name('Test Room with Properties'))
    rs.update_property({"test": "test"})

    assert RoomService.get_by_name(
        room_name='Test Room with Properties').properties == {"test": "test"}

    cleanup_test_room('Test Room with Properties')


def test_connect_room():
    create_test_room('Test Room North')
    create_test_room('Test Room South')
    char = CharacterService.get_by_username('Test Room North User')

    north_room = RoomService.get_by_name('Test Room North')
    south_room = RoomService.get_by_name('Test Room South')
    rs = RoomService.new(north_room)
    rs.connect(to_room_id=south_room.id, name='Breezeway', reversible=True, owner=char.id)

    portals = PortalService.get_by_room(north_room.id)

    assert len(portals) == 1
    assert portals[0].name == 'Breezeway'
    assert portals[0].reversible is True
    assert portals[0].from_room.name == "Test Room North"
    assert portals[0].to_room.name == "Test Room South"
    assert portals[0].owner.name == "Test Room North User"

    cleanupPortals = Portal.objects(owner=str(char.id))
    for a in cleanupPortals:
        a.delete()

    cleanup_test_room('Test Room with Properties')
    cleanup_test_room('Test Room North')
    cleanup_test_room('Test Room South')


def test_dig_room():
    create_test_room('Boring')
    char = CharacterService.get_by_username('Boring User')
    room = RoomService.get_by_name('Boring')

    rs = RoomService.new(room)
    rs.dig(new_room=RoomCreateDTO(owner=str(char.id),
                                  name="The New Room",
                                  description="This is the dug room!",
                                  visible=True),
           portal=PortalUpdateDTO(owner=str(char.id),
                                  name="Northeast",
                                  alias_to=['NE'],
                                  alias_from=['SW'])
           )

    new_room = RoomService.get_by_name('The New Room')

    pprint(new_room)
    # assert len(portals) == 1
    # assert portals[0].name == 'Breezeway'
    # assert portals[0].reversible is True
    # assert portals[0].from_room.name == "Test Room North"
    # assert portals[0].to_room.name == "Test Room South"
    #

    cleanupPortals = Portal.objects(owner=str(char.id))
    for a in cleanupPortals:
        a.delete()
    cleanup_test_room('Boring')
    cleanup_test_room('The New Room')
