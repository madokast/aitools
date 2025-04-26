"""
环境变量工具类
"""

import os

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()

__NOT_SET = object()

def get_env(key, default=__NOT_SET):
    value = os.environ.get(key, default)
    if value is __NOT_SET:
        raise ValueError(f"Environment variable {key} is not set")
    return value

PROJECT_NAME = get_env("PROJECT_NAME", "Madoka")

LOGGER_LEVEL = get_env("LOGGER_LEVEL", "INFO")

