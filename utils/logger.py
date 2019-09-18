import logging
import colorlog
import os.path
from datetime import datetime


class WebDrLogger:
    def __init__(self, name):
        self.name = name
        self.bold_seq = '\033[1m'
        self.log_format = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.colorlog_format = (
            '{}'
            '%(log_color)s '
            '{}'.format(self.bold_seq, self.log_format)
        )
        colorlog.basicConfig(format=self.colorlog_format)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(self.log_format)
        # self.save_logs_in_file(self.logger, self.formatter)

    @staticmethod
    def save_logs_in_file(logger, formatter):
        log_folder = os.path.abspath(os.path.join(__file__, "../../log_folder"))
        log_file = os.path.join(log_folder,
                                "{}_.log".format(datetime.now().strftime('%y-%m-%d_%H:%M:%S')))

        filehandler = logging.FileHandler(log_file, mode="w")
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    def info(self, info):
        self.logger.info(info)