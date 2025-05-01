"""
LLM 提示词
帮用户学习单词，首先调用工具查找单词是否已经存在，存在则输出已有内容；否则，告诉我单词常见的含义和例句，按照 markdown 格式显示：
```md
中文含义1。
- 英文例句1
- 英文例句2

中文含义2。
- 英文例句3
- 英文例句4
```

当询问到用户已经理解单词含义后，调用工具查询单词的曲折变形，然后添加到笔记中，格式如下
```
---
aliases:
- 变形1
- 变形2
---
中文含义1。
- 英文例句1
- 英文例句2

中文含义2。
- 英文例句3
- 英文例句4
```

注意不要将前后的三反引号 "````" 输入到笔记中。

添加笔记成功后，告知用户，并在聊天中给出添加的完整的笔记内容。
"""

from mcp.server.fastmcp import FastMCP
from madokast.tools.utils.english_word.meanings import get_english_meanings
from madokast.tools.utils.english_word.one_meaning import word_one_meaning_async
from madokast.tools.utils.english_word.inflections import get_english_inflections
from madokast.tools.utils.english_word.obsidian_english_words import add_word_markdown, get_word_markdown

# 初始化 FastMCP server
mcp = FastMCP("word")

# mcp_config = {
#     "mcpServers": {
#         "weather": {
#             "command": "uv",
#             "args": [
#                 "--directory",
#                 r"C:\Users\57856\Documents\GitHub\aitools",
#                 "run",
#                 "-m",
#                 "madokast.tools.mcp.word_mcp",
#             ]
#         }
#     }
# }
# print(f"mcp_config: {mcp_config}")

@mcp.tool("Check-Learned", description="""查看一个单词是否已经学习过""")
def check_learned(word:str) -> str:
    """检查一个单词是否已经学习过"""
    md = get_word_markdown(word)
    if md is None:
        return f"单词 {word} 还没有学习过"
    else:
        return f"单词 {word} 已经学习过。笔记内容如下：\n{md}"

# @mcp.tool("Meaning", description="""获取单词最常见的含义""")
# async def one_meaning(word:str) -> str:
#     return await word_one_meaning_async(word)

# @mcp.tool("Meanings", description="""获取单词变形和常见的含义及其例句""")
def meanings(word:str) -> str:
    inf = get_word_inflections(word)
    return f"单词变形: {inf}\n\n{get_english_meanings(word)}"

@mcp.tool("New-Word", description="""添加一个新单词到笔记本中。传入单词原型 lemma 和单词解释 explanation。
其中单词解释由两部分组成，一个是单词的变形，一个是单词的含义和例句。
单词的变形，对于动词来说是现在时态、过去时态和过去分词；对于名词来说是单数和复数；对于形容词来说是副词形式、比较级和最高级。
这些变形，写在 `aliases:` 换行后面，用 markdown 形式的无序列表中，并前后用 `---` 分隔。
如果单词的变形和单词原型相同，则不用列出，例如 read 的过去式和过去分词都不用列出。
这些变形，如果有相同的，只需要列出一次。有些变形可能不存在，例如 unique 的比较级和最高级不存在，不用列出。
在 `---` 分隔符号后，尽可能简短地写出单词的含义，之后换行在用无序列表的形式写出1个例句。
如果单词的含义不止一个，则换行两次，继续写出下一个含义和例句。
从最常用的含义开始写，生僻的含义不用写出。
下面给出一些例子，例子位于 `>>>>>` 和 `<<<<<` 之间。
>>>>> 
单词原型 lemma：abort
单词解释 explanation：
---
aliases:
- abruptly
---
突然的。
- His abrupt departure is bound to raise questions.
<<<<<<

下面是另一个例子
>>>>> 
单词原型 lemma：abort
单词解释 explanation：
---
aliases:
- abortions
---
堕胎。
- Abortion is restricted in some American states.

失败。
- This project is a complete abortion.
>>>>>""")
def add(lemma:str, explanation:str) -> str:
    return add_word_markdown(word=lemma, markdown=explanation)

@mcp.tool("Inflections", description="""获取一个单词的所有变形。""")
def get_word_inflections(lemma:str) -> str:
    inf = get_english_inflections(lemma)
    if len(inf) == 0:
        return f"单词 {lemma} 没有变形"
    return ", ".join(inf)

if __name__ == "__main__":
    mcp.run(transport='stdio')

