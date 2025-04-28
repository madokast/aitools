"""
利用大模型获取单词含义
"""

from madokast.llm.quick_chat import chat

def get_english_meanings(word:str) -> str:
    """
    获取单词的含义
    """
    prompt = f"""请帮我获取单词 {word} 的中文含义，以 markdown 格式输出。
格式如下：
==
中文含义1。
- 英文例句1
- 英文例句2

中文含义2。
- 英文例句3
- 英文例句4
==
注意生僻含义不用给出，只给出常见的含义，相似的含义尽可能合并。每个含义描述尽可能简短，采用中文短语，而不是句子。
英文例句尽可能简单常见，和单词语境最切合。有时甚至可以不是完整的句子。
例如 abortion 这个单词
==
堕胎。
- Abortion is restricted in some American states.

失败。
- This project is a complete abortion.
==
再例如 agency
==
代理。
- a successful advertising agency

政府部门。
- the government agency
==
再例如 align
==
对齐，一致。
- Domestic prices have been aligned with those in world markets. 
==
现在请你获取单词 {word} 的含义，按照上述格式输出，注意不包含前后的 `==` 分隔符。
"""
    return chat(prompt, stream_mode=False)

