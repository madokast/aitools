import madokast.utils.logger as _ # init
from madokast.utils.cli import CLI, Command
from madokast.llm.quick_chat import chat, chat_loop
from madokast.tools.utils.english_inflections import get_english_inflections

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

if __name__ == '__main__':
    cli.run()


