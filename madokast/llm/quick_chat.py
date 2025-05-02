"""
快速访问 chat 和 chat_loop，加快启动速度
"""

from madokast.utils.thread_local import ThreadLocal

def create_chat_bot():
    from.chat_bot import ChatBot
    return ChatBot()

chat_bot = ThreadLocal(factory=create_chat_bot)

def chat(prompt:str, stream_mode:bool=True, stream_prefix:str='AI: ',
              stream_consumer=lambda s:print(s, end='', flush=True)):
    return chat_bot.chat(prompt, stream_mode=stream_mode, 
                         stream_prefix=stream_prefix, stream_consumer=stream_consumer, 
                         clean_messages=True)

def chat_loop():
    chat_bot.chat_loop()
