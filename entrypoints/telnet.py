import asyncio
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
        loop = asyncio.get_event_loop()
        server = loop.run_until_complete(
            telnetlib3.create_server(
                port=int(os.environ.get("TELNET_PORT", DEFAULT_LISTEN_PORT)),
                shell=self.shell,
                term=DEFAULT_TERM_TYPE
            )
        )
        loop.run_until_complete(server.wait_closed())

    async def shell(self, reader, writer):
        return await TelnetService(self.instance_name, reader, writer).thread()
