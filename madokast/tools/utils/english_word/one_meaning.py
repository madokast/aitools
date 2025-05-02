"""
获取英文单词含义
"""

import asyncio
from googletrans import Translator

translator = Translator()

async def word_one_meaning_async(word:str) -> str:
    result = await translator.translate(word, src='en', dest='zh-cn')
    return result.text

def get_word_one_meaning(word:str) -> str:
    return asyncio.run(word_one_meaning_async(word))
