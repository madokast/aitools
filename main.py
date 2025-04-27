import madokast.utils.logger as _ # init
from madokast.utils.cli import CLI, Command
from madokast.llm.quick_chat import chat, chat_loop
from madokast.tools.utils.english_word.meanings import get_english_meanings
from madokast.tools.utils.english_word.one_meaning import get_word_one_meaning
from madokast.tools.utils.english_word.inflections import get_english_inflections

cli = CLI()
cli.add_command(Command(
    full_name="chat_loop",
    abbr_name="c",
    help="chat with llm",
    target=chat_loop
))

cli.add_command(Command(
    full_name="query",
    abbr_name="q",
    help="query llm",
    target=chat
))

cli.add_command(Command(
   full_name="inflections",
   abbr_name="i",
   help="get inflections of a word",
   target=lambda word: print(get_english_inflections(word))
))

cli.add_command(Command(
   full_name="one-meaning",
   abbr_name="om",
   help="get one meaning of a word",
   target=lambda word: print(get_word_one_meaning(word)) 
))

cli.add_command(Command(
   full_name="meanings",
   abbr_name="m",
   help="get meanings of a word",
   target=lambda word: print(get_english_meanings(word)) 
))

if __name__ == '__main__':
    cli.run()


