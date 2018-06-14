import config
import logging

logging.basicConfig(filename='logfile_' + config.PROJECT_NAME + '.log', level=logging.INFO)
logger = logging.getLogger(config.PROJECT_NAME)
