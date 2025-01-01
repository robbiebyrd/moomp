from email_validator import validate_email, EmailNotValidError

from commands.text.base import Command
from middleware.updater import notify
from models.account import Account, AccountCreateDTO
from models.character import Character, CharacterCreateDTO
from services.account import AccountService
from services.authn import AuthNService
from services.character import CharacterService
from services.session import TextSession
from services.telnet.input import input_line
from templates.character.text import CharacterTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer

ren = TextGraphicsRenderer()

PASSWORD_POLICY = "default"


class RegisterCommand(Command):
    command_prefixes = ["register"]

    @classmethod
    async def register_account(cls, session):
        while True:
            email_input = await input_line(session, "Email Address: ")
            already_emails = Account.objects(email=email_input)
            if len(already_emails) > 0:
                session.writer.write(
                    f"That email address is already taken, please try another one.{ren.nl}"
                )
                continue
            try:
                email_validated = validate_email(
                    email_input, check_deliverability=False
                )
                email_input = email_validated.normalized
            except EmailNotValidError:
                session.writer.write(f"That email address is invalid.{ren.nl}")
                continue
            break
        while True:
            password_input = str(
                await input_line(session, "Password: ", mask_character="*")
            )
            if not AuthNService().password_policy(password_input, PASSWORD_POLICY):
                session.writer.write(
                    f"That password does not meet the complexity requirements.{ren.nl}"
                )
                continue
            break
        new_account = AccountService.register(
            AccountCreateDTO(
                email=email_input,
                password=str(password_input),
                instance_id=str(session.instance.id),
            )
        )

        notify("Account", new_account, "Created")
        session.writer.write(
            f"Your account has been created! {ren.nl} Now, create a character to use in-game.{ren.nl}"
        )
        return new_account

    @classmethod
    async def register_character(cls, session, new_account):
        while True:
            character_name_input = await input_line(
                session,
                ren.ct("Give your new character a username: ", "blue"),
                required=True,
            )

            if Character.objects(name=character_name_input).count() == 0:
                break

            session.writer.write(
                f"That character username is already taken, please try another one.{ren.nl}"
            )

        display_name_input = await input_line(
            session, "Give your new character a friendly display name: "
        )

        return CharacterService.register(
            character=CharacterCreateDTO(
                name=character_name_input,
                display=display_name_input,
                account_id=str(new_account.id),
            )
        )

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        account = await cls.register_account(session)
        character = await cls.register_character(session, account)
        if character:
            writer.write(CharacterTextTemplate(session).get(character, "new"))
        else:
            writer.write(f"Something went wrong. {ren.nl}")
