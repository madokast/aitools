
import logging

from madokast.utils.env import LOGGER_LEVEL, PROJECT_NAME

logger = logging.getLogger(PROJECT_NAME)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    sh = logging.StreamHandler()
    sh.setLevel(LOGGER_LEVEL)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s"))
    
    logger.addHandler(sh)

    logger.debug("Init logging")
    

