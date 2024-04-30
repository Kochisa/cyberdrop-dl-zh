from __future__ import annotations

from typing import TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, NumberValidator
from rich.console import Console

if TYPE_CHECKING:
    from cyberdrop_dl.managers.manager import Manager

console = Console()


def edit_global_settings_prompt(manager: Manager) -> None:
    """Edit the authentication values"""
    while True:
        console.clear()
        console.print("编辑全局设置")
        action = inquirer.select(
            message="你想做什么？",
            choices=[
                Choice(1, "编辑通用设置"),
                Choice(2, "编辑速率限制设置"),
                Choice(3, "完成"),
            ],
        ).execute()

        # Edit General Settings
        if action == 1:
            edit_general_settings_prompt(manager)

        # Edit Rate Limiting Settings
        elif action == 2:
            edit_rate_limiting_settings_prompt(manager)

        # Done
        elif action == 3:
            manager.config_manager.write_updated_global_settings_config()
            break


def edit_general_settings_prompt(manager: Manager) -> None:
    """Edit the general settings"""
    console.clear()
    console.print("编辑通用设置")
    allow_insecure_connections = inquirer.confirm("允许不安全的连接吗？").execute()
    user_agent = inquirer.text(
        message="用户代理:",
        default=manager.config_manager.global_settings_data['General']['user_agent'],
        validate=EmptyInputValidator("输入不应为空")
    ).execute()
    proxy = inquirer.text(
        message="代理:",
        default=manager.config_manager.global_settings_data['General']['proxy']
    ).execute()
    max_filename_length = inquirer.number(
        message="最大文件名长度:",
        default=int(manager.config_manager.global_settings_data['General']['max_file_name_length']),
        float_allowed=False,
    ).execute()
    max_folder_name_length = inquirer.number(
        message="最大文件夹名长度:",
        default=int(manager.config_manager.global_settings_data['General']['max_folder_name_length']),
        float_allowed=False,
    ).execute()
    required_free_space = inquirer.number(
        message="所需空闲空间（GB）:",
        default=int(manager.config_manager.global_settings_data['General']['required_free_space']),
        float_allowed=False,
    ).execute()

    manager.config_manager.global_settings_data['General']['allow_insecure_connections'] = allow_insecure_connections
    manager.config_manager.global_settings_data['General']['user_agent'] = user_agent
    manager.config_manager.global_settings_data['General']['proxy'] = proxy
    manager.config_manager.global_settings_data['General']['max_filename_length'] = int(max_filename_length)
    manager.config_manager.global_settings_data['General']['max_folder_name_length'] = int(max_folder_name_length)
    manager.config_manager.global_settings_data['General']['required_free_space'] = int(required_free_space)


def edit_progress_settings_prompt(manager: Manager) -> None:
    """Edit the progress settings"""
    console.clear()
    console.print("编辑进度设置")
    refresh_rate = inquirer.number(
        message="刷新率:",
        default=int(manager.config_manager.global_settings_data['Progress_Options']['refresh_rate']),
        float_allowed=False,
    ).execute()

    manager.config_manager.global_settings_data['Progress_Options']['refresh_rate'] = int(refresh_rate)


def edit_rate_limiting_settings_prompt(manager: Manager) -> None:
    """Edit the rate limiting settings"""
    console.clear()
    console.print("编辑速率限制设置")
    connection_timeout = inquirer.number(
        message="连接超时（秒）:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['connection_timeout']),
        float_allowed=False,
    ).execute()
    read_timeout = inquirer.number(
        message="读取超时（秒）:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['read_timeout']),
        float_allowed=False,
    ).execute()
    download_attempts = inquirer.number(
        message="下载尝试次数:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['download_attempts']),
        float_allowed=False,
    ).execute()
    rate_limit = inquirer.number(
        message="每秒最大请求数量:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['rate_limit']),
        float_allowed=False,
    ).execute()
    throttle = inquirer.number(
        message="下载阶段请求之间的延迟时间（秒）:",
        default=float(manager.config_manager.global_settings_data['Rate_Limiting_Options']['download_delay']),
        float_allowed=True,
    ).execute()

    max_simultaneous_downloads = inquirer.number(
        message="同时下载的最大数量:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['max_simultaneous_downloads']),
        float_allowed=False,
    ).execute()
    max_simultaneous_downloads_per_domain = inquirer.number(
        message="每个域名同时下载的最大数量:",
        default=int(manager.config_manager.global_settings_data['Rate_Limiting_Options']['max_simultaneous_downloads_per_domain']),
        float_allowed=False,
    ).execute()

    manager.config_manager.global_settings_data['Rate_Limiting_Options']['connection_timeout'] = int(connection_timeout)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['read_timeout'] = int(read_timeout)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['download_attempts'] = int(download_attempts)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['rate_limit'] = int(rate_limit)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['download_delay'] = float(throttle)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['max_simultaneous_downloads'] = int(max_simultaneous_downloads)
    manager.config_manager.global_settings_data['Rate_Limiting_Options']['max_simultaneous_downloads_per_domain'] = int(max_simultaneous_downloads_per_domain)
