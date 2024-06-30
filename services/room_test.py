from models.portal import PortalUpdateDTO, Portal
from models.room import RoomCreateDTO, RoomUpdateDTO, Room
from services.character import CharacterService
from services.character_test import create_test_character, cleanup_test_character
from services.portal import PortalService
from services.room import RoomService
from utils.db import connect_db

connect_db()


def cleanup_test_room(room: Room):
    room = RoomService.get_by_id(room.id)
    if room:
        RoomService.remove(room.id)
    cleanup_test_character(room.name + " User")


def create_test_room(room_name: str):
    create_test_character(room_name + " User")
    char = CharacterService.get_by_username(room_name + " User")
    room = RoomCreateDTO(
        name=room_name + " Room",
        description="The " + room_name + " Room",
        owner=str(char.id),
        visible=True,
        parent_id="",
    )
    return RoomService.create(room)


def test_create_room():
    cs = create_test_room("Test")

    assert cs.name == "Test Room"
    assert cs.description == "The Test Room"
    assert cs.visible is True

    cleanup_test_room(cs)


def test_rename_room():
    csi = create_test_room("Test")

    RoomService.update(room=RoomUpdateDTO(id=str(csi.id), name="Test Room Renamed"))
    csn = RoomService.get_by_id(csi.id)

    assert csn.name == "Test Room Renamed"

    cleanup_test_room(csi)


def test_update_room():
    csi = create_test_room("Test")

    RoomService.update(
        room=RoomUpdateDTO(
            id=str(csi.id),
            name="Test Room 2",
            description="Test Room 2",
        )
    )
    cs = RoomService.get_by_id(csi.id)

    assert cs.name == "Test Room 2"
    assert cs.description == "Test Room 2"

    cleanup_test_room(csi)


def test_update_room_properties():
    rs = create_test_room("Test Properties")

    RoomService.update_property(room_id=rs.id, properties={"test": "test"})

    assert RoomService.get_by_id(rs.id).properties == {"test": "test"}

    cleanup_test_room(rs)


def test_connect_room():
    north_room = create_test_room("Test North")
    south_room = create_test_room("Test South")
    char = CharacterService.get_by_username("Test North User")

    RoomService.connect(
        north_room.id,
        PortalUpdateDTO(
            name="Breezeway",
            owner=str(char.name),
            to_room=str(south_room.id),
            reversible=True,
        ),
    )

    portals = PortalService.get_by_room(north_room.id)

    assert len(portals) == 1
    assert portals[0].name == "Breezeway"
    assert portals[0].reversible is True
    assert portals[0].from_room.name == "Test North Room"
    assert portals[0].to_room.name == "Test South Room"
    assert portals[0].owner.name == "Test North User"

    cleanup_portals = Portal.objects(owner=str(char.id))
    for a in cleanup_portals:
        a.delete()

    cleanup_test_room(north_room)
    cleanup_test_room(south_room)


def test_dig_room():
    room = create_test_room("Boring")
    char = CharacterService.get_by_username("Boring User")

    portal = RoomService.dig(
        room.id,
        new_room=RoomCreateDTO(
            owner=str(char.id),
            name="The New Room",
            description="This is the dug room!",
            visible=True,
        ),
        portal=PortalUpdateDTO(
            owner=str(char.id),
            reversible=True,
            name="Northeast",
            from_room=str(room.id),
            alias_to=["NE"],
            alias_from=["SW"],
        ),
    )

    new_room = RoomService.get_by_id(portal.to_room.id)

    assert portal.name == "Northeast"
    assert portal.reversible is True
    assert portal.from_room.name == "Boring Room"
    assert portal.to_room.name == "The New Room"

    cleanup_test_room(room)
    cleanup_test_room(new_room)
    portal.delete()
