from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler

import calendar
import functools
import logging as log
import os
import time

constants = dict(
    info = dict(
        epoch = calendar.timegm(time.gmtime()),
        host = 'localhost',
        port = 8384
    ),
    log = dict(
        folder_name = '../log/',
        file_extension = 'log',
        max_file_size = 25 * 1024 * 1024,
        max_file_count = 50
    ),
    opt = dict(
        folder_name = '../opt/',
        file_extension = 'json',
        file_prefix = 'scvg'
    ),
    db = dict(
        url = 'mongodb://app_svg:app_svg_123@localhost:8386/scavenger',
        name = 'scavenger'
    ),
    executor = ThreadPoolExecutor(
        max_workers=20,
        thread_name_prefix='scvg'
    ),
)

def build_file_path(folder, extension, suffix = None):
    return '{}/{}_{}{}.{}'.format(
        folder,
        constants.get('opt').get('file_prefix'),
        constants.get('info').get('epoch'),
        '' if not suffix else '_{}'.format(suffix),
        extension
    )

constants.get('log')['file_path'] = build_file_path(
    constants.get('log').get('folder_name'),
    constants.get('log').get('file_extension')
)
constants.get('opt')['file_path'] = functools.partial(
    build_file_path,
    constants.get('opt').get('folder_name'),
    constants.get('opt').get('file_extension')
)

def create_if_missing(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def initialize() -> None:
    create_if_missing(constants.get('log').get('folder_name'))
    create_if_missing(constants.get('opt').get('folder_name'))
    rotating_log_handler = RotatingFileHandler(
        filename=constants.get('log').get('file_path'),
        maxBytes=constants.get('log').get('max_file_size'),
        backupCount=constants.get('log').get('max_file_count')
    )
    log.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)-5s [%(threadName)s | %(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=log.DEBUG,
        handlers=[
            rotating_log_handler
        ]
    )
