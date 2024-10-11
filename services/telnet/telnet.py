import os
from datetime import datetime

from Cheetah.Template import Template
from ansi_escapes import ansiEscapes as ae
from colored import Fore as Fg
from colored import Style as Sty

from commands import base
from models.instance import Instance
from services.mqtt import MQTTService
from services.session import TextSession
from services.telnet.auth_n import login, logout
from services.telnet.mqtt import refresh_subscriptions
from templates.room.text import RoomText
from templates.utils.text.color import ColorTextRenderer
from utils.db import connect_db

connect_db()
renderer = ColorTextRenderer()
ct = renderer.colorize


class TelnetService:
    session: TextSession | None = None

    def __init__(self, instance_name, reader, writer, session=None) -> None:
        if reader is None or writer is None:
            return
        self.session = session if session is not None else TextSession()
        self.session.reader = reader
        self.session.writer = writer
        self.session.instance = Instance.objects(name=instance_name).first()
        self.session.mqtt_client = MQTTService(
            os.environ.get("MQTT_HOST"), os.environ.get("MQTT_PORT"), self.session
        ).client()
        self.session.mqtt_client.loop_start()

    def write_line(self, message, add_newline: bool = True):
        if not isinstance(message, list):
            message = [message]
        for msg in message:
            self.session.writer.write(str(msg) + (renderer.nl if add_newline else ""))

    async def thread(self):
        try:
            colors = self.session.colors

            if msg := self.session.instance.properties['msg_connect']:
                t = Template(msg, searchList={"instance": self.session.instance, "fg": Fg})
                self.write_line(str(t))

            # Attempt to log in
            self.session.character = await login(self.session)
            line = ""

            self.write_line(
                RoomText.get(self.session.character.room, self.session.character),
                add_newline=False
            )

            while True:
                await refresh_subscriptions(self.session)

                # Get input one character at a time.
                char_input = await self.session.reader.read(1)

                # If the input is empty, assume a network disconnection.
                if len(char_input) == 0:
                    logout(self.session)
                    self.session.writer.close()
                    self.session.mqtt_client.disconnect()
                    break

                # Set the window's session size.
                self.session.size = [
                    self.session.writer.get_extra_info("cols"),
                    self.session.writer.get_extra_info("rows"),
                ]

                # Match against our control characters
                match ord(char_input):
                    case 27:  # Escape
                        # Reload the character and show the Room text again
                        self.session.character.reload()
                        self.write_line(
                            RoomText.get(
                                self.session.character.room, self.session.character
                            )
                        )
                    case 8 | 127:  # Backspace/Delete
                        # Remove the last entered character from the display and line buffer
                        line = line[:-1]
                        self.write_line(
                            ae.cursorBackward(1) + ae.eraseEndLine, add_newline=False
                        )
                    case 11:  # Vertical Tab
                        # Show session history
                        self.write_line(
                            "\r\n".join(self.session.input_history) + "\r\n"
                        )
                    case 10 | 13:  # Enter
                        # Pressing Enter triggers the processing of the line
                        # Reload the character document to update any changes that have happened.
                        self.session.character.reload()

                        # Add the line to the session history
                        self.session.input_history.append((line, datetime.now()))

                        # Clear the line and reinsert with the line buffer to fix any input issues
                        self.write_line(
                            "".join(
                                [
                                    ae.eraseLine,
                                    ae.cursorTo(0),
                                    ct(line, renderer.color_theme.input),
                                    Sty.reset,
                                ]
                            ),
                        )

                        # If a valid command prefix isn't found, but an exit has been referenced,
                        # modify the line to include the 'move' command to the line.
                        line = (
                            f"@move {line}"
                            if self.command_is_an_exit(line, self.session)
                            else line
                        )

                        # Look over every command module and attempt to see if the command prefix matches our input.
                        if hasattr(cmd_mod := self.commands(line), "telnet"):
                            await cmd_mod.telnet(
                                self.session.reader,
                                self.session.writer,
                                self.session.mqtt_client,
                                line,
                                self.session,
                            )
                        else:
                            self.write_line("I'm sorry, I didn't understand that.")

                        # Clear the line and we start all over again
                        line = ""
                    case _:  # Any other character
                        char = str(char_input)
                        # Any other characters input be added to the line buffer
                        self.session.writer.echo(ct(char, renderer.color_theme.inputActive))
                        line += char
        finally:
            pass

    @classmethod
    def command_is_an_exit(cls, line, session):
        return not cls.commands(
            line
        ) and line.strip().lower() in RoomText.get_exit_aliases(
            session.character.room, True, True
        )

    @staticmethod
    def commands(line: str):
        stripped_line = line.strip().lower()

        # Get all commands
        command_modules = base.get_command_modules()

        for cmd in command_modules:
            if stripped_line in cmd.command_prefixes or any(
                    stripped_line.startswith(prefix) for prefix in cmd.command_prefixes
            ):
                return cmd
