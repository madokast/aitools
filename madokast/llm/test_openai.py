"""
在 .env 配置
OPENAI_API_KEY=sk-x
OPENAI_API_BASE=https://
"""

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain.chat_models import init_chat_model

model = init_chat_model(
        model='gpt-4o-mini', 
        model_provider='openai',
        base_url=os.environ['OPENAI_API_BASE'],
    )

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
    HumanMessage(content="Translate this sentence from English to Chinese. I love programming.")
]

for chunk in model.stream(messages):
    print(chunk.content, end="", flush=True)


