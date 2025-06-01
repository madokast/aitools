"""
环境变量工具类
"""

import os

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()

__NOT_SET = object()

def get_env(key:str, default:object=__NOT_SET) -> str:
    value = os.environ.get(key, default)
    if value is __NOT_SET:
        raise ValueError(f"Environment variable {key} is not set")
    return str(value)

PROJECT_NAME:str = str(get_env("PROJECT_NAME", "Madoka"))

LOGGER_LEVEL:str = str(get_env("LOGGER_LEVEL", "INFO"))

