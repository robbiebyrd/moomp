from models.character import Character
from services.authn import AuthNService
from services.telnet.input import parse_input_type, input_line, select
from templates.utils.text.color import ColorTextRenderer
from utils.db import connect_db

connect_db()

renderer = ColorTextRenderer()
ct = renderer.colorize


async def login(session):
    autologin = ["wizard@yourhost.com", "wizard"]
    while (
            True
    ):  # This should be a count. We should error out after x number of login tries
        if autologin:
            account = AuthNService.authorize(*autologin)
        else:
            email = await input_line(session, "Email address: ", on_new_line=False)
            password = await input_line(session, "Password: ", "*", on_new_line=False)
            account = AuthNService.authorize(email, password)

        if account is None:
            session.writer.write(
                f"Your email address and password were not accepted. Please try again."
                f" {renderer.nl}"
            )
        else:
            break

    while True:
        characters = AuthNService.characters(account)

        character_input = await select(
            session,
            options=[f"{x.name}" for x in characters],
            message="Select a Character: ",
            colors=renderer.color_groups.get('brightness').get('darker')
        )

        character_input = parse_input_type(character_input)

        if isinstance(character_input, int) and len(characters) >= character_input:
            character = characters[character_input - 1]
            break

        character = Character.objects(name=character_input, account=account).first()
        if character is None:
            session.writer.write(f"I could not find that character. {renderer.nl}")
        else:
            break

    character.online = True
    character.save()

    session.writer.write(
        f"You are logged in as {character.display} ({character.name}).{renderer.nl}"
    )
    return character


def logout(session):
    session.writer.write(f"Goodbye! {renderer.nl}")
    session.character.online = False
    session.character.save()
    session.mqtt_client.loop_stop()
    session.writer.close()

# async def register(self):
#     while True:
#         email_input = await self.input_line("Email Address: ")
#         already_emails = Character.objects(email=email_input)
#         if len(already_emails) > 0:
#             session.writer.write("That email address is already taken, please try another one.")
#             continue
#         break
#
#     while True:
#         character_name_input = await self.input_line("Username: ", required=True, on_new_line=True)
#         already_character_name = Character.objects(name=character_name_input)
#         if len(already_character_name) > 0:
#             session.writer.write("That character name is already taken, please try another one.")
#             continue
#         break
#
#     password_input = await self.input_line("Password: ", mask_character="*")
#     display_name_input = await self.input_line("Display Name: ")
#
#     char = CharacterService.register(
#         user=CharacterCreateDTO(
#             name=character_name_input,
#             display=display_name_input,
#             password=password_input,
#             email=email_input,
#         )
#     )
#     return char
