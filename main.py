import argparse

from entrypoints.telnet import TelnetServer
from utils.clean import clean
from utils.migrate import migrate

parser = argparse.ArgumentParser(prog="MOOMP", description="A simple MOO-like server, written in Python using MongoDB.")
parser.add_argument("command", choices=["dev", "clean", "migrate", "telnet", 'script'])
parser.add_argument("instance", nargs='?', default=None)


def main():
    args = parser.parse_args()

    match args.command:
        case "dev":
            clean()
            migrate()
            TelnetServer(args.instance).serve()
        case "clean":
            clean()
        case "migrate":
            migrate()
        case "telnet":
            TelnetServer(args.instance).serve()
        case _:
            return


if __name__ == "__main__":
    main()
