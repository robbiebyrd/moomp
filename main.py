import argparse

from entrypoints.seed import Seeder
from entrypoints.telnet import TelnetServer
from utils.check import check
from utils.clean import clean
from utils.migrate import migrate

parser = argparse.ArgumentParser(prog="MOOMP", description="A simple MOO-like server, written in Python using MongoDB.")
parser.add_argument("command", choices=["seed", "dev", "clean", "migrate", "telnet", "script", "check"])
parser.add_argument("instance", nargs='?', default=None)
parser.add_argument("--seed_file", nargs='?', default=None)


def main():
    args = parser.parse_args()

    match args.command:
        case "check":
            check()
        case "seed":
            clean()
            if args.seed_file is None:
                print('The argument --seed_file is required.')
            else:
                Seeder(args.seed_file).seed()
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
