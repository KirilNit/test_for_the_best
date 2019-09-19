import logging
import os.path
from datetime import datetime
import sys


class WebDrLogger:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        empty = logging.StreamHandler("")
        ch = logging.StreamHandler(sys.stderr)
        f_handler = logging.FileHandler("myoutput.txt")
        ch.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(f_handler)

    def info(self, info):
        self.logger.info(info)
