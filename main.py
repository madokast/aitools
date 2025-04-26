import madokast.utils.logger as _ # init
from madokast.utils.cli import CLI, Command
from madokast.llm.quick_chat import chat, chat_loop

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

if __name__ == '__main__':
    cli.run()


