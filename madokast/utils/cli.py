"""
命令行工具
"""

import sys
from collections import OrderedDict
from pydantic import BaseModel, model_validator, BeforeValidator
from typing import Optional, Dict, Annotated, Any
from madokast.utils.logger import logger

class Command(BaseModel):
    """
    命令
    """

    # 命令名字，例如 --help
    full_name:str

    # 命令缩写，例如 -h
    abbr_name:Optional[str] = None

    # 命令描述
    help:Optional[str] = None

    # 命令函数
    target:Annotated[Any, BeforeValidator(lambda x: x)]

    def __str__(self):
        return f"{self.full_name} {self.abbr_name} {self.help}"
    
    def __repr__(self):
        return f"{self.full_name} {self.abbr_name}"


class CLI(BaseModel):
    """
    命令行交互
    """

    # 命令名字
    name:str = "ait"

    # 命令描述
    description:str = ""

    # full 名称命令列表
    full_cmd_dict:Dict[str, Command] = OrderedDict()

    # abbr 名称命令列表
    abbr_cmd_dict:Dict[str, Command] = OrderedDict()

    @model_validator(mode='after')
    def init(self) -> 'CLI':
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
            print(f"command {name} not found")
            self.help()
            return
        
        cmd.target(*args)

