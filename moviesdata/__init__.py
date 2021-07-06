import logging

logger = logging
# logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger.basicConfig(filename = 'standard.log',filemode='w',format="%(asctime)s -%(name)s- Line no.%(lineno)d - %(filename)s - %(levelname)s - %(message)s", level=logging.INFO)