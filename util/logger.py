import logging.config


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('converter')
