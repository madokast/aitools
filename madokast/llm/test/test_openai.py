"""
在 .env 配置
OPENAI_API_KEY=sk-x
OPENAI_API_BASE=https://

脚本执行方法 python -m madokast.llm.test.test_openai
"""

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

model_name = os.environ['MODEL_NAME']
model_provider = os.environ['MODEL_PROVIDER']
base_url = os.environ['API_BASE_URL']

extra = {}
if base_url:
    extra['base_url'] = base_url

model:BaseChatModel = init_chat_model(
        model=model_name, 
        model_provider=model_provider,
        base_url=base_url,
        **extra
    )

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
    HumanMessage(content="Translate this sentence from English to Chinese. I love programming.")
]

new_system_message = SystemMessage(content="")
for chunk in model.stream(messages):
    print(chunk.content, end="|", flush=True)
    new_system_message.content += chunk.content

print()
print(new_system_message.content)

messages.append(new_system_message)

