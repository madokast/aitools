"""
获取单词的曲折变形
"""

from typing import List

def get_english_inflections(word:str) -> List[str]:
    from word_forms.lemmatizer import get_word_forms
    all_inf = set()
    for values in get_word_forms(word).values():
        all_inf |= values
    return list(all_inf)