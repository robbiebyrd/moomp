from models.object import ObjectCreateDTO
from services.character_test import create_test_character, cleanup_test_character
from services.object import ObjectService
from utils.db import connect_db

connect_db()


def create_test_object(name: str):
    object_owner = create_test_character(name + " User")
    obj = ObjectCreateDTO(
        name=name,
        owner=str(object_owner.id),
        description=name + " Object",
        properties={"custom_prop": name},
    )
    return ObjectService.create(obj)


def cleanup_test_object(test_obj):
    cleanup_test_character(test_obj.name + " User")
    ObjectService.remove(test_obj.id)


def test_remove_user():
    test_obj = create_test_object("deleteme")
    ObjectService.remove(test_obj.id)

    assert ObjectService.get_by_id(test_obj.id) is None
    cleanup_test_object(test_obj)


# def test_update_user():
#     create_test_character('Test')
#     csu = CharacterService.new('Test')
#     csu.update(
#         user=CharacterUpdateDTO(
#             name="Test2",
#             display="Test User Test2",
#         )
#     )
#     cs = CharacterService.get_by_username('Test2')
#
#     assert cs.name == 'Test2'
#     assert cs.display == 'Test User Test2'
#
#     cleanup_test_character('Test2')
#
#
# def test_remove_user():
#     create_test_character('deleteme')
#     CharacterService.remove('deleteme')
#
#     assert CharacterService.get_by_username(
#         username='Test') is None
#     cleanup_test_character('deleteme')
#
#
# def test_rename_user():
#     create_test_character('RenameMe')
#     cs = CharacterService.new('RenameMe')
#     cs.rename('YouRenamedMe')
#
#     assert CharacterService.get_by_username(
#         username='YouRenamedMe') is not None
#     assert CharacterService.get_by_username(
#         username='RenameMe') is None
#     cleanup_test_character('YouRenamedMe')
#
#
# def test_update_user_properties():
#     create_test_character('PropertyUser')
#     cs = CharacterService(CharacterService.get_by_username('PropertyUser'))
#     cs.update_property({"test": "test"})
#
#     assert CharacterService.get_by_username(
#         username='PropertyUser').properties == {"test": "test"}
#     cleanup_test_character('PropertyUser')
