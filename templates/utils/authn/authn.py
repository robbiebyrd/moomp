import json
import os

from templates.utils.authn.config import ConfigAuthN


class AuthNUtils:
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = 'authn.json'

        self.config = ConfigAuthN.model_validate(
            json.load(open(f'{os.path.dirname(os.path.realpath(__file__))}/{config_file}')))
