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

from pathlib import Path
from typing import Dict, Optional
from ..print_exception import print_exception
import tqdm

# Obsidian 根目录
Obsidian_Root_Dir = r"/mnt/c/Users/madokast/Documents/GitHub/siyuan/obsidian"
# Obsidian_Root_Dir = r"C:\other_programs\siyuan\siyuan\obsidian"


# 单词目录
English_word_Dir = Path(Obsidian_Root_Dir).joinpath("Dict", "English")

# 新增的单词，放在 Temp_English_word_Dir 下
Temp_English_word_Dir = Path(Obsidian_Root_Dir).joinpath("Dict")

# 单词原型
BaseEnglishWord = str

# 单词原型 和 单词变形
AnyEnglishWord = str

# 所有的单词，value 是 BaseEnglishWord，加上 .md 可以得到单词的路径
All_English_word:Dict[AnyEnglishWord, BaseEnglishWord] = {}

New_English_word:Dict[AnyEnglishWord, BaseEnglishWord] = {}

def __init() -> None:
    """
    获取所有的英文单词
    """
    if All_English_word:
        return # 如果已经初始化过了，就不再初始化
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def search_all_words(dir:Path, target:Dict[AnyEnglishWord, BaseEnglishWord]):
        """
        并发查找 dir 下的所有文件
        """
        def search_file(file:Path) -> Dict[AnyEnglishWord, BaseEnglishWord]:
            """
            查找单个文件
            """
            base_english_word = file.stem
            result = {base_english_word: base_english_word}
            with file.open("r", encoding="utf-8") as f:
                in_word_list = False
                for line in f:
                    if line.startswith("---"):
                        if not in_word_list:
                            in_word_list = True
                        else:
                            break
                    elif in_word_list and line.startswith("-"):
                        word = line.strip()[1:].strip()
                        if word:
                            result[word] = base_english_word
            return result
        # 查找 dir 下的所有文件
        all_files = list(dir.glob("*.md"))
        if not all_files:
            return
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(search_file, file) for file in all_files]
            for future in tqdm.tqdm(as_completed(futures), total=len(futures), desc=f"Searched words in {dir}"):
                result = future.result()
                target.update(result)
    
    # def search_all_words(dir:Path, target:Dict[AnyEnglishWord, BaseEnglishWord]):
    #     # 查找 dir 下的所有文件
    #     for file in tqdm.tqdm(list(dir.glob("*.md"))):
    #         # 文件名就是 BaseEnglishWord
    #         base_english_word = file.stem
    #         target[base_english_word] = base_english_word
    #         # 读取文件内容
    #         with file.open("r", encoding="utf-8") as f:
    #             for line in f:
    #                 # 读取单词的不同变形
    #                 in_word_list = False
    #                 if line.startswith("---"):
    #                     if not in_word_list:
    #                         in_word_list = True
    #                     else:
    #                         break
    #                 elif in_word_list:
    #                     # 读取单词变形
    #                     if line.startswith("-"):
    #                         word = line.strip()[1:].strip()
    #                         if word:
    #                             target[word] = base_english_word

    search_all_words(English_word_Dir, All_English_word)
    search_all_words(Temp_English_word_Dir, All_English_word)

@print_exception
def get_word_markdown(word:AnyEnglishWord) -> Optional[str]:
    """
    获取单词的 markdown 内容
    """
    __init()
    base_english_word = All_English_word.get(word, None)
    if word != base_english_word:
        base_english_word = New_English_word.get(word, None)
        if word != base_english_word:
            return None

    # 读取文件内容
    file = English_word_Dir.joinpath(f"{base_english_word}.md")
    with file.open("r", encoding="utf-8") as f:
        return f.read()

@print_exception
def add_word_markdown(word:AnyEnglishWord, markdown:str) -> str:
    """
    添加单词的 markdown 内容
    如果单词已经存在，返回已有的内容
    如果单词不存在，返回添加成功
    """
    __init()
    if word in All_English_word:
        content = get_word_markdown(word)
        return f"单词 {word} 已存在:\n{content}"
    # 写入文件内容
    file = Temp_English_word_Dir.joinpath(f"{word}.md")
    with file.open("w", encoding="utf-8") as f:
        f.write(markdown)
    return f"单词 {word} 成功添加"


if __name__ == "__main__":
    __init()
    for item in list(All_English_word.items())[:10]:
        print(item)
        print(get_word_markdown(item[0]))

