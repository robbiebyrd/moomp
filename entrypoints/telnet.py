import asyncio
import os

import telnetlib3

from services.telnet import TelnetService

DEFAULT_LISTEN_PORT = 7890
DEFAULT_TERM_TYPE = "kterm-color"


class TelnetServer:

    @classmethod
    def serve(cls):
        new_port = int(os.environ.get("TELNET_PORT", 7890))
        if not new_port:
            new_port = DEFAULT_LISTEN_PORT
        loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(port=new_port, shell=cls.shell, term=DEFAULT_TERM_TYPE)
        server = loop.run_until_complete(coro)
        loop.run_until_complete(server.wait_closed())

    @classmethod
    async def shell(cls, reader, writer):
        return await TelnetService(reader, writer).thread()
