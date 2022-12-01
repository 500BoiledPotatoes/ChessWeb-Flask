import logging
from flask.logging import default_handler
import os

from logging.handlers import RotatingFileHandler
from logging import StreamHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, 'logs')

LOG_PATH_ALL = os.path.join(LOG_PATH, 'all.log')

LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10


class Logger(object):

    def init_app(self, app):
        app.logger.removeHandler(default_handler)
        app.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(thread)d:%(threadName)s] [%(filename)s:%(module)s:%(funcName)s] '
            '[%(levelname)s]: %(message)s'
        )

        file_handler = RotatingFileHandler(
            filename=LOG_PATH_ALL,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        for logger in (
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')

        ):
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
