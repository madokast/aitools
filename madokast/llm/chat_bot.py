"""
最简单的命令行对话程序
"""

import os
from typing import List, Optional, NoReturn
from pydantic import BaseModel, model_validator, ConfigDict
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from madokast.utils.logger import logger

class ChatBot(BaseModel):

    # pydantic 配置，允许任意类型
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # 模型提供商，例如 openai
    model_provider:Optional[str] = None
    
    # 模型名，例如 gpt-3.5-turbo
    model_name:Optional[str] = None
    
    # base_url，实现第三方的代理
    base_url:Optional[str] = None

    # 模型
    model:Optional[BaseChatModel] = None

    # 消息列表
    messages:List[HumanMessage|SystemMessage] = []

    # 模型初始信息
    system_message:str = "You are a helpful assistant. You can help me by answering my questions. You can also ask me questions."

    @model_validator(mode='after')
    def init_model(self):

        # 加载 .env 中的环境变量
        from dotenv import load_dotenv
        load_dotenv()

        if not self.model_provider:
            self.model_provider = os.environ['MODEL_PROVIDER']

        if not self.model_name:
            self.model_name = os.environ['MODEL_NAME']

        if not self.base_url:
            self.base_url = os.environ['API_BASE_URL']
        
        logger.info(f"Create model {self.model_provider} {self.model_name}")

        extra = {}
        if self.base_url:
            extra['base_url'] = self.base_url

        self.model:BaseChatModel = init_chat_model(
            model=self.model_name,
            model_provider=self.model_provider,
            **extra
        )

        self.messages = [
            SystemMessage(content=self.system_message) 
        ]

        return self

    def chat(self, prompt:str, stream_mode:bool=True, stream_prefix:str='AI: ',
              stream_consumer=lambda s:print(s, end='', flush=True)) -> str:
        """
        对话
        """
        self.messages.append(HumanMessage(content=prompt))
        if stream_mode:
            response = ""
            stream_consumer(stream_prefix)
            for chunk in self.model.stream(self.messages):
                stream_consumer(chunk.content)
                response += chunk.content
            stream_consumer('\n')
            self.messages.append(SystemMessage(content=response))
            return response
        else:
            response = self.model.invoke(self.messages)
            self.messages.append(SystemMessage(content=response.content))
            return response.content
        
    def chat_loop(self) -> NoReturn:
        """
        对话循环
        """
        while True:
            try:
                prompt = input(">> ")
                self.chat(prompt, stream_mode=True)
            except KeyboardInterrupt:
                break


def chat(prompt:str):
    chat_bot = ChatBot()
    chat_bot.chat(prompt)

def chat_loop():
    chat_bot = ChatBot()
    chat_bot.chat_loop()

