from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator, NumberValidator
from rich.console import Console

from cyberdrop_dl.utils.dataclasses.supported_domains import SupportedDomains

if TYPE_CHECKING:
    from typing import Dict

    from cyberdrop_dl.managers.manager import Manager

console = Console()


def create_new_config_prompt(manager: Manager) -> None:
    """创建新的配置文件"""
    console.clear()
    console.print(f"创建新的配置文件")
    config_name = inquirer.text(
        message="请输入配置文件名:",
        validate=EmptyInputValidator("输入不能为空")
    ).execute()
    if (manager.path_manager.config_dir / config_name).is_dir():
        console.print(f"名称为 '{config_name}' 的配置文件已存在！")
        inquirer.confirm(message="按回车返回主菜单。").execute()
        return
    manager.config_manager.change_config(config_name)
    edit_config_values_prompt(manager)


def edit_config_values_prompt(manager: Manager) -> None:
    """编辑配置值"""
    config = manager.config_manager.settings_data

    while True:
        console.clear()
        console.print(f"编辑配置值")
        action = inquirer.select(
            message="您想要做什么?",
            choices=[
                Choice(1, "编辑下载选项"),
                Choice(2, "编辑输入/输出文件路径"),
                Choice(3, "编辑日志文件命名/路径"),
                Choice(4, "编辑文件大小限制"),
                Choice(5, "编辑忽略选项"),
                Choice(6, "编辑运行时选项"),
                Choice(7, "编辑排序选项"),
                Choice(8, "完成"),
            ], long_instruction="箭头键: 导航 | 回车键: 选择",
        ).execute()

        # 编辑下载选项
        if action == 1:
            edit_download_options_prompt(config)

        # 编辑输入/输出文件路径
        elif action == 2:
            edit_input_output_file_paths_prompt(config)

        # 编辑日志文件命名/路径
        elif action == 3:
            edit_log_file_naming_path_prompt(config)

        # 编辑文件大小限制
        elif action == 4:
            edit_file_size_limits_prompt(config)

        # 编辑忽略选项
        elif action == 5:
            edit_ignore_options_prompt(config)

        # 编辑运行时选项
        elif action == 6:
            edit_runtime_options_prompt(config)

        # 编辑排序选项
        elif action == 7:
            edit_sort_options_prompt(config)

        # 完成
        elif action == 8:
            manager.config_manager.settings_data = config
            manager.config_manager.write_updated_settings_config()
            return


def edit_download_options_prompt(config: Dict) -> None:
    """编辑下载选项"""
    console.clear()
    action = inquirer.checkbox(
        message="选择要启用的下载选项:",
        choices=[
            Choice(value="block_download_sub_folders",
                   name="阻止下载子文件夹",
                   enabled=config["Download_Options"]["block_download_sub_folders"]),
            Choice(value="disable_download_attempt_limit",
                   name="禁用下载尝试限制",
                   enabled=config["Download_Options"]["disable_download_attempt_limit"]),
            Choice(value="disable_file_timestamps",
                   name="禁用文件时间戳编辑",
                   enabled=config["Download_Options"]["disable_file_timestamps"]),
            Choice(value="include_album_id_in_folder_name",
                   name="在文件夹名中包含专辑ID",
                   enabled=config["Download_Options"]["include_album_id_in_folder_name"]),
            Choice(value="include_thread_id_in_folder_name",
                   name="在文件夹名中包含线程ID",
                   enabled=config["Download_Options"]["include_album_id_in_folder_name"]),
            Choice(value="remove_domains_from_folder_names",
                   name="从文件夹名中删除域名",
                   enabled=config["Download_Options"]["remove_domains_from_folder_names"]),
            Choice(value="remove_generated_id_from_filenames",
                   name="从文件名中删除生成的ID",
                   enabled=config["Download_Options"]["remove_generated_id_from_filenames"]),
            Choice(value="scrape_single_forum_post",
                   name="爬取单个论坛帖子",
                   enabled=config["Download_Options"]["scrape_single_forum_post"]),
            Choice(value="separate_posts",
                   name="将帖子分隔到文件夹中",
                   enabled=config["Download_Options"]["separate_posts"]),
            Choice(value="skip_download_mark_completed",
                   name="跳过下载并标记为已完成",
                   enabled=config["Download_Options"]["skip_download_mark_completed"]),
        ], long_instruction="箭头键: 导航 | TAB键: 选择 | 回车键: 确认",
    ).execute()

    for key in config["Download_Options"].keys():
        config["Download_Options"][key] = False

    for key in action:
        config["Download_Options"][key] = True


def edit_input_output_file_paths_prompt(config: Dict) -> None:
    """编辑输入/输出文件路径"""
    console.clear()
    console.print("编辑输入/输出文件路径")
    input_file = inquirer.filepath(
        message="输入文件路径:",
        default=str(config['Files']['input_file']),
        validate=PathValidator(is_file=True, message="输入不是一个文件")
    ).execute()
    download_folder = inquirer.text(
        message="下载文件夹路径:",
        default=str(config['Files']['download_folder']),
        validate=PathValidator(is_dir=True, message="输入不是一个文件夹")
    ).execute()

    config['Files']['input_file'] = Path(input_file)
    config['Files']['download_folder'] = Path(download_folder)


def edit_log_file_naming_path_prompt(config: Dict) -> None:
    """编辑日志文件命名/路径"""
    console.clear()
    console.print("编辑日志文件命名/路径")
    log_folder = inquirer.filepath(
        message="日志文件夹路径:",
        default=str(config['Logs']['log_folder']),
        validate=PathValidator(is_dir=True, message="输入不是一个文件夹")
    ).execute()
    main_log_filename = inquirer.text(
        message="主日志文件名:",
        default=config['Logs']['main_log_filename'],
        validate=EmptyInputValidator("输入不能为空"),
    ).execute()
    last_forum_post_filename = inquirer.text(
        message="最后一个论坛帖子日志文件名:",
        default=config['Logs']['last_forum_post_filename'],
        validate=EmptyInputValidator("输入不能为空"),
    ).execute()
    unsupported_urls_filename = inquirer.text(
        message="不支持的URL日志文件名:",
        default=config['Logs']['unsupported_urls_filename'],
        validate=EmptyInputValidator("输入不能为空"),
    ).execute()
    download_error_urls_filename = inquirer.text(
        message="下载错误的URL日志文件名:",
        default=config['Logs']['download_error_urls_filename'],
        validate=EmptyInputValidator("输入不能为空"),
    ).execute()
    scrape_error_urls_filename = inquirer.text(
        message="爬取错误的URL日志文件名:",
        default=config['Logs']['scrape_error_urls_filename'],
        validate=EmptyInputValidator("输入不能为空"),
    ).execute()

    config['Logs']['log_folder'] = Path(log_folder)
    config['Logs']['main_log_filename'] = main_log_filename
    config['Logs']['last_forum_post_filename'] = last_forum_post_filename
    config['Logs']['unsupported_urls_filename'] = unsupported_urls_filename
    config['Logs']['download_error_urls_filename'] = download_error_urls_filename
    config['Logs']['scrape_error_urls_filename'] = scrape_error_urls_filename


def edit_file_size_limits_prompt(config: Dict) -> None:
    """编辑文件大小限制"""
    console.clear()
    console.print("编辑文件大小限制")
    maximum_image_size = inquirer.number(
        message="请输入最大图片大小:",
        default=int(config['File_Size_Limits']['maximum_image_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()
    maximum_video_size = inquirer.number(
        message="请输入最大视频大小:",
        default=int(config['File_Size_Limits']['maximum_video_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()
    maximum_other_size = inquirer.number(
        message="请输入其他文件类型的最大大小:",
        default=int(config['File_Size_Limits']['maximum_other_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()
    minimum_image_size = inquirer.number(
        message="请输入最小图片大小:",
        default=int(config['File_Size_Limits']['minimum_image_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()
    minimum_video_size = inquirer.number(
        message="请输入最小视频大小:",
        default=int(config['File_Size_Limits']['minimum_video_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()
    minimum_other_size = inquirer.number(
        message="请输入其他文件类型的最小大小:",
        default=int(config['File_Size_Limits']['minimum_other_size']),
        validate=NumberValidator(),
        long_instruction="此值以字节为单位 (0 表示无限制)",
    ).execute()

    config['File_Size_Limits']['maximum_image_size'] = int(maximum_image_size)
    config['File_Size_Limits']['maximum_video_size'] = int(maximum_video_size)
    config['File_Size_Limits']['maximum_other_size'] = int(maximum_other_size)
    config['File_Size_Limits']['minimum_image_size'] = int(minimum_image_size)
    config['File_Size_Limits']['minimum_video_size'] = int(minimum_video_size)
    config['File_Size_Limits']['minimum_other_size'] = int(minimum_other_size)


def edit_ignore_options_prompt(config: Dict) -> None:
    """编辑忽略选项"""
    console.clear()
    console.print("编辑忽略选项")
    action = inquirer.checkbox(
        message="选择要启用的忽略选项:",
        choices=[
            Choice(value="exclude_videos",
                   name="不下载视频文件",
                   enabled=config["Ignore_Options"]["exclude_videos"]),
            Choice(value="exclude_images",
                   name="不下载图片文件",
                   enabled=config["Ignore_Options"]["exclude_images"]),
            Choice(value="exclude_audio",
                   name="不下载音频文件",
                   enabled=config["Ignore_Options"]["exclude_audio"]),
            Choice(value="exclude_other",
                   name="不下载其他文件",
                   enabled=config["Ignore_Options"]["exclude_other"]),
            Choice(value="ignore_coomer_ads",
                   name="在爬取时忽略 coomer 广告",
                   enabled=config["Ignore_Options"]["ignore_coomer_ads"]),
        ], long_instruction="箭头键: 移动 | TAB: 选择 | 回车键: 确认",
    ).execute()

    for key in config["Ignore_Options"].keys():
        config["Ignore_Options"][key] = False

    for key in action:
        config["Ignore_Options"][key] = True

    skip_choices = list(SupportedDomains.supported_hosts)
    skip_choices.insert(0, "无")
    skip_hosts = inquirer.fuzzy(
        choices=skip_choices,
        multiselect=True,
        message="选择在爬取时要忽略的网站:",
        long_instruction="箭头键: 移动 | 输入: 过滤 | TAB: 选择 | 回车键: 确认",
    ).execute()

    skip_hosts = [host for host in skip_hosts if host in SupportedDomains.supported_hosts]
    config["Ignore_Options"]["skip_hosts"] = skip_hosts

    only_choices = list(SupportedDomains.supported_hosts)
    only_choices.insert(0, "无")
    only_hosts = inquirer.fuzzy(
        choices=only_choices,
        multiselect=True,
        message="选择要从中爬取的网站:",
        long_instruction="箭头键: 移动 | 输入: 过滤 | TAB: 选择 | 回车键: 确认",
    ).execute()

    only_hosts = [host for host in only_hosts if host in SupportedDomains.supported_hosts]
    config["Ignore_Options"]["only_hosts"] = only_hosts


def edit_runtime_options_prompt(config: Dict) -> None:
    """编辑运行时选项"""
    console.clear()
    console.print("编辑运行时选项")
    action = inquirer.checkbox(
        message="选择要启用的运行时选项:",
        choices=[
            Choice(value="ignore_history",
                   name="忽略历史记录（之前下载过的文件）",
                   enabled=config["Runtime_Options"]["ignore_history"]),
            Choice(value="skip_check_for_partial_files",
                   name="跳过检查下载文件夹中的部分文件",
                   enabled=config["Runtime_Options"]["skip_check_for_partial_files"]),
            Choice(value="skip_check_for_empty_folders",
                   name="跳过检查下载文件夹中的空文件夹",
                   enabled=config["Runtime_Options"]["skip_check_for_empty_folders"]),
            Choice(value="delete_partial_files",
                   name="删除下载文件夹中的部分文件",
                   enabled=config["Runtime_Options"]["delete_partial_files"]),
            Choice(value="send_unsupported_to_jdownloader",
                   name="将不支持的 URL 发送到 JDownloader 进行下载",
                   enabled=config["Runtime_Options"]["send_unsupported_to_jdownloader"]),
        ], long_instruction="箭头键: 移动 | TAB: 选择 | 回车键: 确认",
    ).execute()

    for key in config["Runtime_Options"].keys():
        config["Runtime_Options"][key] = False

    for key in action:
        config["Runtime_Options"][key] = True


def edit_sort_options_prompt(config: Dict) -> None:
    """编辑排序选项"""
    console.clear()
    console.print("编辑排序选项")
    config["Sorting"]["sort_downloads"] = False
    sort_downloads = inquirer.confirm(message="是否要让 Cyberdrop-DL 为您排序文件?").execute()
    if sort_downloads:
        config["Sorting"]["sort_downloads"] = True
        sort_folder = inquirer.filepath(
            message="输入要将文件排序到的文件夹:",
            default=str(config['Sorting']['sort_folder']),
            validate=PathValidator(is_dir=True, message="输入不是文件夹"),
        ).execute()
        sort_incremementer_format = inquirer.text(
            message="输入排序增量器格式:",
            default=config['Sorting']['sort_incremementer_format'],
            validate=EmptyInputValidator("输入不能为空"),
        ).execute()
        sorted_audio = inquirer.text(
            message="输入要将音频文件排序为的格式:",
            default=config['Sorting']['sorted_audio'],
            validate=EmptyInputValidator("输入不能为空"),
        ).execute()
        sorted_video = inquirer.text(
            message="输入要将视频文件排序为的格式:",
            default=config['Sorting']['sorted_video'],
            validate=EmptyInputValidator("输入不能为空"),
        ).execute()
        sorted_image = inquirer.text(
            message="输入要将图片文件排序为的格式:",
            default=config['Sorting']['sorted_image'],
            validate=EmptyInputValidator("输入不能为空"),
        ).execute()
        sorted_other = inquirer.text(
            message="输入要将其他文件排序为的格式:",
            default=config['Sorting']['sorted_other'],
            validate=EmptyInputValidator("输入不能为空"),
        ).execute()

        config['Sorting']['sort_folder'] = Path(sort_folder)
        config['Sorting']['sort_incremementer_format'] = sort_incremementer_format
        config['Sorting']['sorted_audio'] = sorted_audio
        config['Sorting']['sorted_video'] = sorted_video
        config['Sorting']['sorted_image'] = sorted_image
        config['Sorting']['sorted_other'] = sorted_other
