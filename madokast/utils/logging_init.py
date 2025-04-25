
import os
import logging

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()
print("Load environment variables")

logger = logging.getLogger(os.environ['PROJECT_NAME'])
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    sh = logging.StreamHandler()

    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s"))
    
    logger.addHandler(sh)

    logger.debug("Init logging")
    

