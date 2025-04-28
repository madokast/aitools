"""
快速访问 chat 和 chat_loop，加快启动速度
"""

chat_bot = None

def chat(prompt:str, stream_mode:bool=True, stream_prefix:str='AI: ',
              stream_consumer=lambda s:print(s, end='', flush=True)):
    # 延迟导入
    global chat_bot 
    if chat_bot is None:
        from .chat_bot import ChatBot
        chat_bot = ChatBot()
    return chat_bot.chat(prompt, stream_mode=stream_mode, 
                         stream_prefix=stream_prefix, stream_consumer=stream_consumer, 
                         clean_messages=True)

def chat_loop():
    # 延迟导入
    global chat_bot
    if chat_bot is None:
        from.chat_bot import ChatBot
        chat_bot = ChatBot()
    chat_bot.chat_loop()
