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
    """程序的主提示"""
    action = inquirer.select(
        message="您想做什么？",
        choices=[
            Choice(1, "下载"),
            Choice(2, "下载（所有配置）"),
            Choice(3, "重试下载失败的文件"),
            Choice(4, "编辑URL文件"),
            Separator(),
            Choice(5, f"选择配置（当前: {manager.config_manager.loaded_config})"),
            Choice(6, "更改URLs.txt文件和下载位置"),
            Choice(7, "管理配置"),
            Separator(),
            Choice(8, "导入 Cyberdrop_V4 项目"),
            Choice(9, "捐赠"),
            Choice(10, "退出"),
        ], long_instruction="箭头键: 导航 | 回车: 选择",
    ).execute()

    return action


def manage_configs_prompt() -> int:
    """管理配置提示"""
    console.clear()
    action = inquirer.select(
        message="您想做什么？",
        choices=[
            Choice(1, "更改默认配置"),
            Choice(2, "创建新配置"),
            Choice(3, "删除配置"),
            Separator(),
            Choice(4, "编辑配置"),
            Choice(5, "编辑身份验证值"),
            Choice(6, "编辑全局值"),
            Choice(7, "完成"),
        ], long_instruction="箭头键: 导航 | 回车: 选择",
    ).execute()

    return action


def select_config_prompt(configs: List) -> str:
    """从配置列表中选择配置文件"""
    choice = inquirer.fuzzy(
        choices=configs,
        multiselect=False,
        validate=lambda result: len(result) > 0,
        invalid_message="需要选择一个配置。",
        message="选择一个配置文件：",
        long_instruction="箭头键: 导航 | 输入: 过滤 | TAB: 选择, 回车: 完成选择",
    ).execute()

    return choice


def import_cyberdrop_v4_items_prompt(manager: Manager) -> None:
    """导入 Cyberdrop_V4 项目"""
    while True:
        console.clear()
        console.print(f"编辑配置值")
        action = inquirer.select(
            message="您想做什么？",
            choices=[
                Choice(1, "导入配置"),
                Choice(2, "导入 download_history.sql"),
                Choice(3, "完成"),
            ], long_instruction="箭头键: 导航 | 回车: 选择"
        ).execute()

        # 导入配置
        if action == 1:
            new_config_name = inquirer.text(
                message="您想将此配置命名为什么？",
                validate=EmptyInputValidator("输入不能为空"),
            ).execute()

            if (manager.path_manager.config_dir / new_config_name).is_dir():
                console.print(f"名为 '{new_config_name}' 的配置已经存在！")
                inquirer.confirm(message="按回车键返回导入菜单。").execute()
                continue

            home_path = "~/" if os.name == "posix" else "C:\\"
            import_config_path = inquirer.filepath(
                message="选择要导入的配置文件",
                default=home_path,
                validate=PathValidator(is_file=True, message="输入不是文件"),
            ).execute()

            transfer_v4_config(manager, import_config_path, new_config_name)

        # 导入 download_history.sql
        elif action == 2:
            home_path = "~/" if os.name == "posix" else "C:\\"
            import_download_history_path = inquirer.filepath(
                message="选择要导入的 download_history.sql 文件",
                default=home_path,
                validate=PathValidator(is_file=True, message="输入不是文件"),
            ).execute()

            transfer_v4_db(import_download_history_path, manager.path_manager.history_db)

        # 完成
        elif action == 3:
            break


def donations_prompt() -> None:
    """Donations prompt"""
    console.clear()
    console.print("[bold]捐赠[/bold]")
    console.print("")
    console.print("我大约三年前开始制作这个程序，"
                  "\n它已经变得比我想象的还要庞大，我为此感到非常自豪。"
                  "\n我在这个程序上投入了很多时间和精力，我很高兴人们在使用它。"
                  "\n感谢所有支持我的人，"
                  "你们的支持让我有动力继续努力工作。")
    console.print("")
    console.print("如果您想支持我和我的工作，您可以通过以下方式捐赠给我：")
    console.print("BuyMeACoffee: https://www.buymeacoffee.com/juleswinnft")
    console.print("Github Sponsor: https://github.com/sponsors/Jules-WinnfieldX")

    console.print("")
    console.print("谢谢您的支持！")
    console.print("")
    inquirer.confirm(message="按回车键返回主菜单。", vi_mode=manager.vi_mode).execute()
