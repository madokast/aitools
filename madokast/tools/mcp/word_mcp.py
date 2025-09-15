"""
You are a Enlish teacher. User is a Chinese student and now is learning English vocabulary with you.

The user will give you an English word, and you will help the user learn the word in the following steps:

First, you should check if the word has already been learned by calling the tool `Check-Learned`.

If the word has been learned, output the existing content to the user and tell the user that the word has already been learned.

If the word has not been learned, you should call tool `Get-Inflections` to get the inflections of the word.

Then, you should think about the Chinese meaning and example sentences of the word.

And then you should output these in markdown format to user's notebook by calling the tool `Add-Word`.

The markdown content follows the format below:
```md
---
aliases:
- inflection1
- inflection2
- and so on
---
Chinese meaning 1.
- example sentence1
- example sentence2

Chinese meaning 2.
- example sentence3
- example sentence4
```

For example, the inflections, meaning and example sentences of the word "abortion" can be:
aliases:
- abortions
---
堕胎。
- Abortion is restricted in some American states.

失败。
- This project is a complete abortion.

Notice the surrounding triple backticks "```md" and "```" should not be included in the note.

When you have successfully added the note, inform the user and provide the complete content of the added note in the chat.
"""

from mcp.server.fastmcp import FastMCP
from madokast.utils.env import get_env
from madokast.tools.utils.thread_synchronized import Synchronized
from madokast.tools.utils.english_word.inflections import get_english_inflections
from madokast.tools.utils.english_word.obsidian_english_words import add_word_markdown, get_word_markdown

# 初始化 FastMCP server
mcp = FastMCP("word", host="0.0.0.0", port=int(get_env("WORD_MCP_PORT")))

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

@mcp.tool("Check-Learned", description="""Check if a word has been learned. If learned, return the content of the note; if not learned, return a message indicating it has not been learned.""")
@Synchronized(key='obsidian')
def check_learned(word:str) -> str:
    md = get_word_markdown(word)
    if not md:
        return f"Word {word} has not been learned."
    else:
        return f"Word {word} has been learned. Here is the content:\n{md}"


@mcp.tool("Get-Inflections", description="""Get the inflections of a word. For example, for the verb 'run', the inflections include 'runs', 'running', 'ran'. For the noun 'cat', the inflection is 'cats'. For the adjective 'happy', the inflections include 'happier', 'happiest', 'happily'. Return the inflections as a comma-separated string. If there are no inflections, return a message indicating that.""")
def get_word_inflections(lemma:str) -> str:
    inf = get_english_inflections(lemma)
    if len(inf) == 0:
        return f"Word {lemma} has no inflections."
    return ", ".join(inf)

@mcp.tool("Add-Word", description="""Add a new word to the notebook. Provide the word's lemma and its explanation.
          
The content of the explanation consists of two parts: the inflections of the word, and the meanings and example sentences of the word.

The inflections of the word are obtained by calling the tool `Get-Inflections`. 

Write the inflections in a markdown unordered list after `aliases:`, and separate this section with `---` before and after.

After the `---` separator, write the Chinese meanings of the word as concisely as possible, followed by example sentences in an unordered list.          
          
If the word has multiple meanings, write each meaning followed by its example sentences in an unordered list.

Here is an example of the explanation content surrounded by `>>>>>` and `<<<<<`:

>>>>> 
word: abrupt
explanation:
---
aliases:
- abruptly
---
突然的。
- His abrupt departure is bound to raise questions.
<<<<<<

And here is a more complete example surrounded by >>>>> and <<<<<. You should follow this format.

>>>>> 
word: abort
explanation:
---
aliases:
- abortions
---
堕胎。
- Abortion is restricted in some American states.

失败。
- This project is a complete abortion.
>>>>>
""")
@Synchronized(key='obsidian')
def add(word:str, explanation:str) -> str:
    return add_word_markdown(word=word, markdown=explanation)


if __name__ == "__main__":
    mcp.run(transport='stdio')

