import datetime
import importlib
import logging

import migrations
from utils.db import connect_db

logger = logging.getLogger(__name__)


def migrate():
    connect_db()
    migrations.__all__.sort()

    for module_path in migrations.__all__:
        module = importlib.import_module("migrations." + module_path)
        if hasattr(module, "run"):
            logging.info(f"[{datetime.datetime.now(datetime.UTC)}] Migrating {module_path}")
            if hasattr(module, "description"):
                logging.info(f"[{datetime.datetime.now(datetime.UTC)}] Description: {module.description()}")
            module.run()
            logging.info(f"[{datetime.datetime.now(datetime.UTC)}] Migrated {module_path}")
        else:
            logging.info(f"[{datetime.datetime.now(datetime.UTC)}] No Run command for migration {module_path}")
