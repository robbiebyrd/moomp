import asyncio
import os

import telnetlib3

from models.instance import Instance
from services.telnet import TelnetService

DEFAULT_LISTEN_PORT = 7890
DEFAULT_TERM_TYPE = "kterm-color"


class TelnetServer:
    instance_name: Instance

    def __init__(self, instance_name):
        self.instance_name = instance_name

    def serve(self):
        new_port = int(os.environ.get("TELNET_PORT", 7890)) or DEFAULT_LISTEN_PORT
        loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(port=new_port, shell=self.shell, term=DEFAULT_TERM_TYPE)
        server = loop.run_until_complete(coro)
        loop.run_until_complete(server.wait_closed())

    async def shell(self, reader, writer):
        return await TelnetService(self.instance_name, reader, writer).thread()
