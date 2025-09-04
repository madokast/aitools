r"""
obsidian 英语单词相关工具

单词以 {单词原型}.md 形式存在 English_word_Dir 中

内容为如下
##################################
---
aliases:
- {单词变形1}
- {单词变形2}
---
含义1。
- 例句

含义2。
- 例句

##################################

单词变形，即动词的不同时态，以及名词的单复数，形容词的比较级最高级副词形式。

多个单词变形，用 markdown 的 `- x` 列表形式写出，放在 `---` 之间。

之后书写单词的含义和例句，例句以 `-` 列表形式写出。

举一个例子

##################################
---
aliases:
- aborts
- aborted
- aborting
---
堕胎，流产。
- tissue from aborted fetuses

停止。
- The decision was made to abort the mission.

##################################

脚本运行方法 
- python -m madokast.tools.utils.obsidian_english_words
- uv --directory C:\Users\57856\Documents\GitHub\aitools\madokast\tools\utils run obsidian_english_words.py
"""

import logging
from pathlib import Path
from typing import Set, Optional, Tuple, List
from ..print_exception import print_exception

# Obsidian 根目录
# Obsidian_Root_Dir = r"/mnt/c/Users/madokast/Documents/GitHub/siyuan/obsidian"
Obsidian_Root_Dir = r"C:\other_programs\siyuan\siyuan\obsidian"


# 单词目录
English_word_Dir = Path(Obsidian_Root_Dir).joinpath("Dict", "English")

# 新增的单词，放在 Temp_English_word_Dir 下
Temp_English_word_Dir = Path(Obsidian_Root_Dir).joinpath("Dict")

# 单词原型
EnglishWord = str

# 所有的单词，加上 .md 可以得到单词的路径
All_English_word:Set[EnglishWord] = set()

def __init() -> None:
    """
    获取所有的英文单词
    """
    if All_English_word:
        return # 如果已经初始化过了，就不再初始化
    
    import time
    start = time.time()

    for file in English_word_Dir.glob("*.md"):
        All_English_word.add(file.stem)
    for file in Temp_English_word_Dir.glob("*.md"):
        All_English_word.add(file.stem)

    end = time.time()
    logging.info(f"init word dict: {end - start:.2f} s")

@print_exception
def get_word_markdown(word:EnglishWord) -> Optional[str]:
    """
    获取单词的 markdown 内容
    """
    __init()
    if word not in All_English_word:
        return None

    # 读取文件内容
    file = English_word_Dir.joinpath(f"{word}.md")
    if file.exists():
        with file.open("r", encoding="utf-8") as f:
            return f.read()
    file = Temp_English_word_Dir.joinpath(f"{word}.md")
    if file.exists():
        with file.open("r", encoding="utf-8") as f:
            return f.read()
    logging.warning(f"{word} not found")
    return None

@print_exception
def add_word_markdown(word:EnglishWord, markdown:str) -> str:
    """
    添加单词的 markdown 内容
    如果单词已经存在，返回已有的内容
    如果单词不存在，返回添加成功
    """
    __init()
    content = get_word_markdown(word)
    if content:
        return f"单词 {word} 已存在:\n{content}"
    # 写入文件内容
    file = Temp_English_word_Dir.joinpath(f"{word}.md")
    with file.open("w", encoding="utf-8") as f:
        f.write(markdown)
    All_English_word.add(word)
    return f"单词 {word} 成功添加"


if __name__ == "__main__":
    __init()
    for item in list(All_English_word.items())[:10]:
        print(item)
        print(get_word_markdown(item[0]))

