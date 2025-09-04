"""
获取单词的曲折变形
"""

from typing import List, Set

def get_english_inflections(word:str) -> List[str]:
    from word_forms.lemmatizer import get_word_forms # type: ignore
    all_inf:Set[str] = set()
    form_words = get_word_forms(word)
    if not form_words:
        return []
    for values in form_words.values(): # type: ignore
        all_inf |= values
    all_inf.remove(word) # 去除原型
    return list(all_inf)
