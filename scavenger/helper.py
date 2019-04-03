from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from logging.handlers import RotatingFileHandler
from pydash import omit
from scavenger.definitions.flusher import Flusher

import calendar
import functools
import logging as log
import os
import time

def is_empty(value):
    return not (isinstance(value, int) or (isinstance(value, str) and value.strip() != '') or (not isinstance(value, str) and value))

def is_str_in(value, ref_values):
    return (value or '').lower() in ref_values

def is_true(value):
    return (isinstance(value, bool) and value) or (isinstance(value, str) and value.lower() == 'true')

def parse_int(num, default=0):
    return default if not num or not num.isdigit() else int(num)

constants = dict(
    info = dict(
        epoch = calendar.timegm(time.gmtime()),
        host = 'localhost',
        port = 8386
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
        url = 'mongodb://{}',
        name = 'scavenger'
    ),
    executor = ThreadPoolExecutor(
        max_workers=20,
        thread_name_prefix='scvg'
    ),
    flush_mode = dict(
        manual		= Flusher.Mode(0, 0),
		immediate	= Flusher.Mode(1, 1),
		frequent	= Flusher.Mode(2000, timedelta(seconds=120)),
		rare		= Flusher.Mode(10000, timedelta(minutes=30)),
		custom		= functools.partial(Flusher.Mode)
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

def create_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)

def initialize():
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

def prune_records(data, unwanted_keys):
    if isinstance(data, dict):
        return omit(data, *unwanted_keys)
    elif isinstance(data, list):
        return list(map(lambda d: prune_records(d, unwanted_keys), data))
    else:
        return data
