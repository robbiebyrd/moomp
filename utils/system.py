import glob
import importlib
from os.path import dirname, basename, isfile, join


def get_modules(file_path):
    dirs = list(filter(lambda x: (not x.endswith('__.py') and not x.endswith('base.py')),
                       [fn for fn in glob.glob(join(dirname(file_path), "*.py"))]))

    return [basename(f)[:-3] for f in dirs if
            isfile(f) and not f.endswith('__init__.py')]


def import_modules(module_list, attribute: str, path_prefix: str, class_posfix: str) -> list:
    modules = []
    for module_path in module_list:
        module = getattr(importlib.import_module(path_prefix + module_path), (module_path.title() + class_posfix))
        if hasattr(module, attribute):
            modules.append(module)
    return modules
