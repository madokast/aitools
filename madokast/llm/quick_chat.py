"""
快速访问 chat 和 chat_loop，加快启动速度
"""

def chat(prompt:str):
    # 延迟导入
    from .chat_bot import ChatBot
    chat_bot = ChatBot()
    chat_bot.chat(prompt)

def chat_loop():
    # 延迟导入
    from.chat_bot import ChatBot
    chat_bot = ChatBot()
    chat_bot.chat_loop()
