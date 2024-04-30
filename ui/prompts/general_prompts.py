from __future__ import annotations

import os
from typing import TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import EmptyInputValidator, PathValidator
from rich.console import Console

from cyberdrop_dl.utils.transfer.transfer_v4_config import transfer_v4_config
from cyberdrop_dl.utils.transfer.transfer_v4_db import transfer_v4_db

if TYPE_CHECKING:
    from typing import List

    from cyberdrop_dl.managers.manager import Manager


console = Console()


def main_prompt(manager: Manager) -> int:
    """Main prompt for the program"""
    action = inquirer.select(
        message="你想做什么？",
        choices=[
            Choice(1, "下载"),
            Choice(2, "下载（所有配置）"),
            Choice(3, "重试失败的下载"),
            Choice(4, "编辑URL文件"),
            Separator(),
            Choice(5, f"选择配置（当前：{manager.config_manager.loaded_config}）"),
            Choice(6, "更改URLs.txt文件和下载位置"),
            Choice(7, "管理配置"),
            Separator(),
            Choice(8, "导入Cyberdrop_V4项目"),
            Choice(9, "捐赠"),
            Choice(10, "退出"),
        ], long_instruction="使用箭头键导航 | 按回车键选择",
    ).execute()

    return action


def manage_configs_prompt() -> int:
    """Manage Configs Prompt"""
    console.clear()
    action = inquirer.select(
        message="你想做什么？",
        choices=[
            Choice(1, "更改默认配置"),
            Choice(2, "创建新配置"),
            Choice(3, "删除配置"),
            Separator(),
            Choice(4, "编辑配置"),
            Choice(5, "编辑认证值"),
            Choice(6, "编辑全局值"),
            Choice(7, "完成"),
        ], long_instruction="使用箭头键导航 | 按回车键选择",
    ).execute()

    return action


def select_config_prompt(configs: List) -> str:
    """Select a config file from a list of configs"""
    choice = inquirer.fuzzy(
        choices=configs,
        multiselect=False,
        validate=lambda result: len(result) > 0,
        invalid_message="需要选择一个配置。",
        message="选择一个配置文件：",
        long_instruction="使用箭头键导航 | 输入：过滤 | 按Tab键选择，按回车键完成选择",
    ).execute()

    return choice


def import_cyberdrop_v4_items_prompt(manager: Manager) -> None:
    """Import Cyberdrop_V4 Items"""
    while True:
        console.clear()
        console.print(f"编辑配置值")
        action = inquirer.select(
            message="你想做什么？",
            choices=[
                Choice(1, "导入配置"),
                Choice(2, "导入download_history.sql"),
                Choice(3, "完成"),
            ], long_instruction="使用箭头键导航 | 按回车键选择"
        ).execute()

        # Import Config
        if action == 1:
            new_config_name = inquirer.text(
                message="这个配置应该叫什么名字？",
                validate=EmptyInputValidator("输入不能为空"),
            ).execute()

            if (manager.path_manager.config_dir / new_config_name).is_dir():
                console.print(f"名为'{new_config_name}'的配置已经存在！")
                inquirer.confirm(message="按回车键返回导入菜单").execute()
                continue

            home_path = "~/" if os.name == "posix" else "C:\\"
            import_config_path = inquirer.filepath(
                message="选择要导入的配置文件",
                default=home_path,
                validate=PathValidator(is_file=True, message="输入不是文件"),
            ).execute()

            transfer_v4_config(manager, import_config_path, new_config_name)

        # Import download_history.sql
        elif action == 2:
            home_path = "~/" if os.name == "posix" else "C:\\"
            import_download_history_path = inquirer.filepath(
                message="选择要导入的download_history.sql文件",
                default=home_path,
                validate=PathValidator(is_file=True, message="输入不是文件"),
            ).execute()

            transfer_v4_db(import_download_history_path, manager.path_manager.history_db)

        # Done
        elif action == 3:
            break


def donations_prompt() -> None:
    """Donations prompt"""
    console.clear()
    console.print("[bold]捐赠[/bold]")
    console.print("")
    console.print("大约三年前我开始制作这个程序，"
                  "\n现在它比我预想的要大得多，我对此感到非常自豪。"
                  "\n我在这个程序上投入了很多时间和精力，我很高兴有人在使用它。"
                  "\n感谢所有支持我的人，这让我有动力继续开发这个程序。")
    console.print("")
    console.print("如果你想支持我和我的工作，可以通过以下方式捐款：")
    console.print("给我买一杯咖啡: https://www.buymeacoffee.com/juleswinnft")
    console.print("GitHub赞助：https://github.com/sponsors/Jules-WinnfieldX")

    console.print("")
    console.print("感谢您的支持！")
    console.print("")
    inquirer.confirm(message="按回车键返回主菜单").execute()
