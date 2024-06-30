from models.character import CharacterCreateDTO, CharacterUpdateDTO
from services.character import CharacterService
from utils.db import connect_db

connect_db()


def create_test_character(username: str):
    CharacterService.remove(username)
    character = CharacterCreateDTO(
        name=username,
        email=username + "@" + username + ".com",
        password=username + "123",
        display="Test User " + username,
        visible=True,
    )
    return CharacterService.register(character)


def cleanup_test_character(username: str):
    CharacterService.remove(username)


def test_create_user():
    create_test_character("Test")
    cs = CharacterService.get_by_username("Test")
    assert cs.name == "Test"
    assert cs.email == "Test@Test.com"
    cleanup_test_character("Test")


def test_update_user():
    create_test_character("Test")
    csu = CharacterService.new("Test")
    csu.update(
        user=CharacterUpdateDTO(
            name="Test2",
            display="Test User Test2",
        )
    )
    cs = CharacterService.get_by_username("Test2")

    assert cs.name == "Test2"
    assert cs.display == "Test User Test2"

    cleanup_test_character("Test2")


def test_remove_user():
    create_test_character("deleteme")
    CharacterService.remove("deleteme")

    assert CharacterService.get_by_username(username="Test") is None
    cleanup_test_character("deleteme")


def test_rename_user():
    create_test_character("RenameMe")
    cs = CharacterService.new("RenameMe")
    cs.rename("YouRenamedMe")

    assert CharacterService.get_by_username(username="YouRenamedMe") is not None
    assert CharacterService.get_by_username(username="RenameMe") is None
    cleanup_test_character("YouRenamedMe")


def test_update_user_properties():
    create_test_character("PropertyUser")
    cs = CharacterService(CharacterService.get_by_username("PropertyUser"))
    cs.update_property({"test": "test"})

    assert CharacterService.get_by_username(username="PropertyUser").properties == {
        "test": "test"
    }
    cleanup_test_character("PropertyUser")
