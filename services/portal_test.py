from models.portal import PortalCreateDTO, PortalUpdateDTO
from services.character_test import create_test_character
from services.portal import PortalService
from services.room_test import create_test_room, cleanup_test_room
from utils.db import connect_db

connect_db()


def create_test_portal(portal_name: str, from_room: str, to_room: str):
    test_char = create_test_character(portal_name + " User")
    portal = PortalCreateDTO(
        name=portal_name,
        owner=str(test_char.id),
        from_room=str(from_room),
        to_room=str(to_room),
        visible=True,
    )
    return PortalService.create(portal)


def cleanup_test_portal(portal):
    # PortalService.remove(portal.id)
    return


def test_create_portal():
    test_room = create_test_room("Create Test Room")
    test_room_2 = create_test_room("Create Test Room 2")
    test_portal = create_test_portal("Test", test_room.id, test_room_2.id)
    cs = PortalService.get_by_id(test_portal.id)
    assert cs.name == "Test"
    cleanup_test_portal(test_portal)
    cleanup_test_room(test_room)


def test_update_portal():
    test_room = create_test_room("Update Test Room")
    test_room_2 = create_test_room("Update Test Room 2")
    test_portal = create_test_portal("Test", test_room.id, test_room_2.id)
    PortalService.update(
        test_portal.id,
        PortalUpdateDTO(
            name="Test2",
            display="Test User Test2",
        ),
    )
    cs = PortalService.get_by_id(test_portal.id)

    assert cs.name == "Test2"

    cleanup_test_portal(test_portal)
    cleanup_test_room(test_room)


def test_remove_portal():
    test_room = create_test_room("Delete Test Room")
    test_room_2 = create_test_room("Delete Test Room 2")
    test_portal = create_test_portal("deleteme", test_room.id, test_room_2.id)
    PortalService.remove(test_portal.id)

    assert PortalService.get_by_id(test_portal.id) is None
    cleanup_test_portal(test_portal)
    cleanup_test_room(test_room)


# def test_rename_portal():
#     create_test_portal("RenameMe")
#     cs = PortalService.new("RenameMe")
#     cs.rename("YouRenamedMe")
#
#     assert PortalService.get_by_username(username="YouRenamedMe") is not None
#     assert PortalService.get_by_username(username="RenameMe") is None
#     cleanup_test_portal("YouRenamedMe")
#
#
# def test_update_portal_properties():
#     create_test_portal("PropertyUser")
#     cs = PortalService(PortalService.get_by_username("PropertyUser"))
#     cs.update_property({"test": "test"})
#
#     assert PortalService.get_by_username(username="PropertyUser").properties == {
#         "test": "test"
#     }
#
#     cleanup_test_portal("PropertyUser")
