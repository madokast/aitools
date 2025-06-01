"""
获取单词的曲折变形
"""

from typing import List, Set

def get_english_inflections(word:str) -> List[str]:
    from word_forms.lemmatizer import get_word_forms # type: ignore
    all_inf:Set[str] = set()
    for values in get_word_forms(word).values(): # type: ignore
        all_inf |= values
    all_inf.remove(word) # 去除原型
    return list(all_inf)
