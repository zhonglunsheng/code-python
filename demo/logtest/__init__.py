import logging

logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

from loguru import logger
log = logger.add('hello.log', format="{time} | {level} | {message}", level="DEBUG", rotation="200 MB", retention="10 days", compression="zip")
logger.debug("That's it, beautiful and simple logging!")

i = 1 / 0