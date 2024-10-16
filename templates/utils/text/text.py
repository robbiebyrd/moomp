from __future__ import annotations

import json
import os

from templates.utils.text.config import ConfigText


class BaseTextRenderer:
    config: ConfigText
    row = 43
    col = 80

    esc = b'\x1b['
    nl = b'\r\n'
    lr = '-' * 80
    lrn = lr + str(nl)
    sp = " "

    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = 'text.json'
        self.config = ConfigText.model_validate(
            json.load(open(f'{os.path.dirname(os.path.realpath(__file__))}/{config_file}')))
        lr_config = self.config.text.line_rule
        if isinstance(lr_config, list) and len(lr_config) == 2 and (
                isinstance(lr_config[0], str) and isinstance(lr_config[1], int)):
            self.lr = lr_config[0] * lr_config[1]
        elif isinstance(lr_config, list) and len(lr_config) == 1 and isinstance(lr_config[0], str):
            self.lr = lr_config[0] * self.col
        elif isinstance(lr_config, str):
            self.lr = lr_config
        else:
            self.lr = '-' * self.col

        self.esc = self.enc(self.config.escape_codes.prefixes.escape)
        self.nl = self.enc(self.config.text.newline)
        self.sp = self.enc(self.config.text.space)
        self.lrn = self.lr + self.nl

    def resize(self, size: list[int]):
        # Any property that needs to be dynamically set based on the width and height
        # (or rows and columns) of a text session can be recalculated here.
        self.col, self.row = size

        lr_char, max_width = self.config.text.line_rule
        self.lr = lr_char * min(size[0], max_width)

    @staticmethod
    def enc(e):
        return bytes(e.encode('utf-8')).decode('unicode-escape')
