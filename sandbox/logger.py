import logging

conf = {
    'filename': '/tmp/log.log',
    'filemode': 'a',
    'level': logging.DEBUG,
    'format': '%(asctime)s %(levelname)s:%(message)s'
}

logging.basicConfig(**conf)

logging.warning('Warning!')

logging.getLogger()