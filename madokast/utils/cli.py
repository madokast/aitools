"""
命令行工具
"""

import sys
from collections import OrderedDict
from typing import Optional, Dict, Callable
from madokast.utils.logger import logger
from madokast.utils.env import PROJECT_NAME

logger.debug("Load cli.py")

class Command:
    """
    命令
    """

    def __init__(self, full_name:str, target:Callable[..., None], 
                 abbr_name:Optional[str] = None, help:Optional[str] = None):
        """
        构建命令
        Args:
            full_name (str): 命令全名
            abbr_name (Optional[str], optional): 命令缩写. Defaults to None.
            help (Optional[str], optional): 命令描述. Defaults to None.
            target (Callable): 命令函数
        """
        self.full_name = full_name
        self.abbr_name = abbr_name
        self.help = help
        self.target = target

    def __str__(self):
        return f"{self.full_name} {self.abbr_name} {self.help}"
    
    def __repr__(self):
        return f"{self.full_name} {self.abbr_name}"


class CLI:
    """
    命令行交互
    """

    def __init__(self, name:str = PROJECT_NAME, description:str = ""):
        """
        构建 CLI
        Args:
            name (str, optional): 名称. Defaults to PROJECT_NAME.
            description (str, optional): 描述. Defaults to "".
        """
        self.name = name
        self.description = description

        # full 名称命令列表
        self.full_cmd_dict:Dict[str, Command] = OrderedDict()

        # abbr 名称命令列表
        self.abbr_cmd_dict:Dict[str, Command] = OrderedDict()
        self.abbr_cmd_dict:Dict[str, Command] = OrderedDict()

        self.__init()

    def __init(self) -> 'CLI':
        """
        初始化
        """
        logger.debug("Init Cli")
        self.add_command(Command(
            full_name="help",
            abbr_name="h",
            help="show help",
            target=self.help
        ))
        return self

    def add_command(self, command:Command) -> None:
        """
        添加命令
        """
        logger.debug(f"Add command {command}")
        full_name = f"--{command.full_name}"
        if full_name in self.full_cmd_dict:
            raise ValueError(f"command {full_name} already exists")
        self.full_cmd_dict[full_name] = command
        if command.abbr_name:
            abbr_name = f"-{command.abbr_name}"
            if abbr_name in self.abbr_cmd_dict:
                raise ValueError(f"command {abbr_name} already exists")
            self.abbr_cmd_dict[abbr_name] = command

    def get_command_by_name(self, name:str) -> Optional[Command]:
        """
        根据名字获取命令
        """
        if name.startswith('--'):
            return self.full_cmd_dict.get(name, None)
        if name.startswith('-'):
            return self.abbr_cmd_dict.get(name, None)
        return None

    def help(self) -> None:
        """
        生成帮助
        """
        print(self.name)
        if self.description:
            print(self.description)
        for cmd in self.full_cmd_dict.values():
            full_cmd = f"--{cmd.full_name}"
            abbr_cmd = f"-{cmd.abbr_name}" if cmd.abbr_name else ''
            print(f"{full_cmd:<20} {abbr_cmd:<10} {cmd.help}")

    def run(self) -> None:
        """
        运行
        """
        logger.debug(f"Run cli {self.name}")
        if len(sys.argv) < 2:
            self.help()
            return
        name = sys.argv[1]
        args = sys.argv[2:]
        cmd = self.get_command_by_name(name)
        if not cmd:
            logger.warning(f"command {name} not found")
            self.help()
            return
        
        cmd.target(*args)

