"""
最简单的命令行对话程序
"""

from madokast.utils.logger import logger
from madokast.utils.env import get_env
from typing import List, Optional, Callable
from pydantic import BaseModel, model_validator, ConfigDict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

logger.debug("Load chat_bot.py")

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
    chat_model:Optional[BaseChatModel] = None # type: ignore

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
            self.model_provider = get_env('MODEL_PROVIDER')

        if not self.model_name:
            self.model_name = get_env('MODEL_NAME')

        if not self.base_url:
            self.base_url = get_env('API_BASE_URL')
        
        logger.info(f"Create model {self.model_provider} {self.model_name}")

        extra = {}
        if self.base_url:
            extra['base_url'] = self.base_url
            
        from langchain.chat_models import init_chat_model
        self.chat_model:BaseChatModel = init_chat_model(
            model=self.model_name,
            model_provider=self.model_provider,
            **extra # type: ignore
        )

        self.messages = [
            SystemMessage(content=self.system_message) 
        ]

        return self

    def clean_messages(self):
        """
        清理消息
        """
        self.messages = [
            SystemMessage(content=self.system_message)
        ]

    def chat(self, prompt:str, stream_mode:bool=True, stream_prefix:str='AI: ',
              stream_consumer:Callable[[str], None]=lambda s:print(s, end='', flush=True), clean_messages:bool=False) -> str:
        """
        对话
        """
        logger.debug(f"User: {prompt}")
        self.messages.append(HumanMessage(content=prompt))
        response:str = ""
        if stream_mode:
            stream_consumer(stream_prefix)
            for chunk in self.chat_model.stream(self.messages):
                stream_consumer(chunk.content) # type: ignore
                response += str(chunk.content) # type: ignore
            stream_consumer('\n')
        else:
            message = self.chat_model.invoke(self.messages)
            response = str(message.content) # type: ignore
        
        logger.debug(f"AI: {response}")
        self.messages.append(SystemMessage(content=response))
        if clean_messages:
            self.clean_messages()
        return response
        
    def chat_loop(self) -> None:
        """
        对话循环
        """
        while True:
            try:
                prompt = input(">> ")
                self.chat(prompt, stream_mode=True)
            except KeyboardInterrupt:
                break

