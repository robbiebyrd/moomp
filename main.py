import argparse

from entrypoints.mqtt import MQTTConsumer
from entrypoints.seed import Seeder
from entrypoints.telnet import TelnetServer
from utils.clean import clean

parser = argparse.ArgumentParser(
    prog="MOOMP",
    description="A simple MOO-like server, written in Python using MongoDB.",
)
parser.add_argument(
    "command", choices=["seed", "dev", "clean", "migrate", "telnet", "script"]
)
parser.add_argument("instance", nargs="?", default=None)
parser.add_argument("--seed_file", nargs="?", default=None)


def main():
    args = parser.parse_args()

    match args.command:
        case "seed":
            if args.seed_file is None:
                print("The argument --seed_file is required.")
            else:
                Seeder(args.seed_file).seed()
        case "dev":
            clean()
            TelnetServer(args.instance).serve()
        case "clean":
            clean()
        case "telnet":
            MQTTConsumer(args.instance).serve()
            TelnetServer(args.instance).serve()
        case _:
            return


if __name__ == "__main__":
    main()
