from commands.base import Command
from services.session import TextSession
from services.telnet import TelnetService


class LogoutCommand(Command):
    command_prefixes = ["logout"]

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: TextSession):
        ts = TelnetService(reader, writer, session)
        ts.logout(mqtt_client)
