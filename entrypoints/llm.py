import os

import telnetlib3

from models.instance import Instance
from services.telnet.telnet import TelnetService

DEFAULT_LISTEN_PORT = 7890
DEFAULT_TERM_TYPE = "kterm-color"


class TelnetServer:
    instance_name: Instance

    def __init__(self, instance_name):
        self.instance_name = instance_name

    def serve(self):
        return telnetlib3.create_server(
                port=int(os.environ.get("TELNET_PORT", DEFAULT_LISTEN_PORT)),
                shell=self.shell,
                term=DEFAULT_TERM_TYPE,
            )

    async def shell(self, reader, writer):
        return await TelnetService(self.instance_name, reader, writer).thread()
