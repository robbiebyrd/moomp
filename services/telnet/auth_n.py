from middleware.updater import notify_and_create_event
from models.character import Character
from services.authn import AuthNService
from services.room import RoomService
from services.telnet.input import input_line, parse_input_type, select
from templates.utils.authn.authn import AuthNUtils
from utils.db import connect_db

connect_db()

# autologin = ["wizard@yourhost.com", "wizard"]
autologin = None

config = AuthNUtils().config


async def login(session):
    for _ in range(5):
        if autologin:
            account = AuthNService.authorize(*autologin)
        else:
            email = await input_line(session, "Email address: ", on_new_line=False)
            password = await input_line(session, "Password: ", "*", on_new_line=False)
            account = AuthNService.authorize(email, password)

        if account:
            break

        session.writer.write(
            f"Your email address and password were not accepted. Please try again."
            f" {session.ren.nl}"
        )
    else:
        session.writer.write(
            f"You are being disconnected after 5 unsuccessful login attempts."
            f" {session.ren.nl}"
        )
        logout(session)
        return

    while True:
        characters = AuthNService.characters(account)

        character_input = await select(
            session,
            options=[f"{x.name}" for x in characters],
            message="Select a Character: ",
            colors=session.ren.colors,
        )

        character_input = parse_input_type(character_input)

        if isinstance(character_input, int) and characters.count() >= character_input:
            character = characters[character_input - 1]
            break

        character = Character.objects(name=character_input, account=account).first()
        if character is None:
            session.writer.write(f"I could not find that character. {session.ren.nl}")
        else:
            break

    character.online = True

    if not character.room:
        character.room = RoomService.get_by_name("Main Entrance")

    character.save()

    session.writer.write(
        f"You are logged in as {character.display} ({character.name}).{session.ren.nl}"
    )
    return character


def logout(session):
    if session.character:
        session.character.online = False
        session.character.save()
        notify_and_create_event(
            session.instance,
            "Room",
            session.character.room,
            "Exited",
            "Character",
            session.character,
        )
        notify_and_create_event(
            session.instance,
            "Character",
            session.character,
            "LoggedOut",
            "Room",
            session.character.room,
        )
        session.mqtt_client.loop_stop()
    if session.writer:
        session.writer.write(f"Goodbye! {session.ren.nl}")
        session.writer.close()
