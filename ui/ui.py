from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from rich.console import Console

from cyberdrop_dl import __version__
from cyberdrop_dl.ui.prompts.settings_authentication_prompts import edit_authentication_values_prompt
from cyberdrop_dl.ui.prompts.general_prompts import (
    main_prompt, select_config_prompt, donations_prompt,
    import_cyberdrop_v4_items_prompt, manage_configs_prompt)
from cyberdrop_dl.ui.prompts.settings_global_prompts import edit_global_settings_prompt
from cyberdrop_dl.ui.prompts.url_file_prompts import edit_urls_prompt
from cyberdrop_dl.ui.prompts.settings_user_prompts import create_new_config_prompt, edit_config_values_prompt

console = Console()

if TYPE_CHECKING:
    from cyberdrop_dl.managers.manager import Manager


def program_ui(manager: Manager):
    """程序界面"""
    while True:
        console.clear()
        console.print(f"[bold]Cyberdrop 下载器 (V{str(__version__)})[/bold]")
        console.print(f"[bold]当前配置:[/bold] {manager.config_manager.loaded_config}")
        
        #vi_mode = manager.config_manager.settings_data['General']['input_file'] if not manager.args_manager.vi_mode else manager.args_manager.vi_mode
            
        action = main_prompt(manager)

        # 下载
        if action == 1:
            break

        # 下载 (所有配置)
        if action == 2:
            manager.args_manager.all_configs = True
            break

        # 重试失败的下载
        elif action == 3:
            manager.args_manager.retry = True
            break
            
        # 对所有配置进行排序
        elif action == 4:
            manager.args_manager.sort_all_configs = True
            manager.args_manager.all_configs = True
            break

        # 编辑URLs
        elif action == 5:
            input_file = manager.config_manager.settings_data['Files']['input_file'] if not manager.args_manager.input_file else manager.args_manager.input_file
            edit_urls_prompt(input_file, manager.vi_mode)

        # 选择配置
        elif action == 6:
            configs = manager.config_manager.get_configs()
            selected_config = select_config_prompt(manager, configs)
            manager.config_manager.change_config(selected_config)

        elif action == 7:
            console.clear()
            console.print("编辑输入/输出文件路径")
            input_file = inquirer.filepath(
                message="输入文件路径:",
                default=str(manager.config_manager.settings_data['Files']['input_file']),
                validate=PathValidator(is_file=True, message="输入不是文件"),
                vi_mode=manager.vi_mode,
            ).execute()
            download_folder = inquirer.text(
                message="下载文件夹路径:",
                default=str(manager.config_manager.settings_data['Files']['download_folder']),
                validate=PathValidator(is_dir=True, message="输入不是文件夹"),
                vi_mode=manager.vi_mode,
            ).execute()

            manager.config_manager.settings_data['Files']['input_file'] = Path(input_file)
            manager.config_manager.settings_data['Files']['download_folder'] = Path(download_folder)
            manager.config_manager.write_updated_settings_config()

        # 管理配置
        elif action == 8:
            while True:
                console.clear()
                console.print("[bold]管理配置[/bold]")
                console.print(f"[bold]当前配置:[/bold] {manager.config_manager.loaded_config}")

                action = manage_configs_prompt(manager)

                # 更改默认配置
                if action == 1:
                    configs = manager.config_manager.get_configs()
                    selected_config = select_config_prompt(manager, configs)
                    manager.config_manager.change_default_config(selected_config)

                # 创建配置
                elif action == 2:
                    create_new_config_prompt(manager)

                # 删除配置
                elif action == 3:
                    configs = manager.config_manager.get_configs()
                    if len(configs) != 1:
                        selected_config = select_config_prompt(manager, configs)
                        if selected_config == manager.config_manager.loaded_config:
                            inquirer.confirm(
                                message="无法删除当前活动配置，请按回车继续。",
                                default=False,
                                vi_mode=manager.vi_mode,
                            ).execute()
                            continue
                        manager.config_manager.delete_config(selected_config)
                    else:
                        inquirer.confirm(
                            message="只有一个配置，请按回车继续。",
                            default=False,
                            vi_mode=manager.vi_mode,
                        ).execute()

                # 编辑配置
                elif action == 4:
                    edit_config_values_prompt(manager)

                # 编辑认证值
                elif action == 5:
                    edit_authentication_values_prompt(manager)

                # 编辑全局设置
                elif action == 6:
                    edit_global_settings_prompt(manager)

                # 完成
                elif action == 7:
                    break

        # 导入 Cyberdrop_V4 项目
        elif action == 9:
            import_cyberdrop_v4_items_prompt(manager)

        # 捐赠
        elif action == 10:
            donations_prompt(manager)

        # 退出
        elif action == 11:
            exit(0)
