from commands.text.base import Command
from services.session import TextSession
from services.telnet.auth_n import logout


class LogoutCommand(Command):
    command_prefixes = ["logout", "quit"]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: TextSession
    ):
        logout(session)
