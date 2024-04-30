from __future__ import annotations

from typing import TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console

from cyberdrop_dl.utils.args.browser_cookie_extraction import get_forum_cookies, get_ddos_guard_cookies
from cyberdrop_dl.managers.manager import Manager

if TYPE_CHECKING:
    from typing import Dict

    from cyberdrop_dl.managers.manager import Manager

console = Console()


def edit_authentication_values_prompt(manager: Manager) -> None:
    """Edit the authentication values"""
    auth = manager.config_manager.authentication_data

    while True:
        console.clear()
        console.print("编辑认证值")
        action = inquirer.select(
            message="你想做什么？",
            choices=[
                Choice(1, "编辑DDOS-Guard Cookie"),
                Choice(2, "编辑论坛认证值"),
                Choice(3, "编辑JDownloader认证值"),
                Choice(4, "编辑Reddit认证值"),
                Choice(5, "编辑GoFile API密钥"),
                Choice(6, "编辑Imgur客户端ID"),
                Choice(7, "编辑PixelDrain API密钥"),
                Choice(8, "完成"),
            ], long_instruction="方向键: 导航 | 回车: 选择"
        ).execute()

        # Edit DDOS-Guard Cookies
        if action == 1:
            edit_ddos_guard_cookies_prompt(manager)

        # Edit Forums
        if action == 2:
            edit_forum_authentication_values_prompt(manager)

        # Edit JDownloader
        elif action == 3:
            edit_jdownloader_authentication_values_prompt(auth)

        # Edit Reddit
        elif action == 4:
            edit_reddit_authentication_values_prompt(auth)

        # Edit GoFile API Key
        elif action == 5:
            console.clear()
            gofile_api_key = inquirer.text(
                message="请输入GoFile API密钥:",
                default=auth["GoFile"]["gofile_api_key"],
                long_instruction="你可以从https://gofile.io/myProfile获取你的高级GoFile API密钥",
            ).execute()
            auth["GoFile"]["gofile_api_key"] = gofile_api_key

        # Edit Imgur Client ID
        elif action == 6:
            console.clear()
            imgur_client_id = inquirer.text(
                message="请输入Imgur客户端ID:",
                default=auth["Imgur"]["imgur_client_id"],
                long_instruction="你可以在https://imgur.com/account/settings/apps创建一个应用并获取你的客户端ID"
            ).execute()
            auth["Imgur"]["imgur_client_id"] = imgur_client_id

        # Edit PixelDrain API Key
        elif action == 7:
            console.clear()
            pixeldrain_api_key = inquirer.text(
                message="请输入PixelDrain API密钥:",
                default=auth["PixelDrain"]["pixeldrain_api_key"],
                long_instruction="你可以在https://pixeldrain.com/user/api_keys获取你的高级API密钥"
            ).execute()
            auth["PixelDrain"]["pixeldrain_api_key"] = pixeldrain_api_key

        # Done
        elif action == 8:
            manager.config_manager.write_updated_authentication_config()
            return


def edit_ddos_guard_cookies_prompt(manager: Manager) -> None:
    """Edit the forum authentication values"""
    while True:
        console.clear()
        console.print("编辑DDOS-Guard Cookie值")
        action = inquirer.select(
            message="你想做什么？",
            choices=[
                Choice(1, "浏览器Cookie提取"),
                Choice(2, "手动输入Cookie值"),
                Choice(3, "完成"),
            ], long_instruction="方向键: 导航 | 回车: 选择"
        ).execute()

        # Browser Cookie Extraction
        if action == 1:
            action = inquirer.select(
                message="我们应该从哪个浏览器加载Cookie？",
                choices=[
                    Choice("chrome", "Chrome"),
                    Choice("firefox", "FireFox"),
                    Choice("edge", "Edge"),
                    Choice("safari", "Safari"),
                    Choice("opera", "Opera"),
                    Choice("brave", "Brave"),
                    Choice(1, "完成"),
                ], long_instruction="方向键: 导航 | 回车: 选择"
            ).execute()

            # Done
            if action == 1:
                continue

            # Browser Selection
            if action == "chrome":
                get_ddos_guard_cookies(manager, "chrome")
            elif action == "firefox":
                get_ddos_guard_cookies(manager, "firefox")
            elif action == "edge":
                get_ddos_guard_cookies(manager, "edge")
            elif action == "safari":
                get_ddos_guard_cookies(manager, "safari")
            elif action == "opera":
                get_ddos_guard_cookies(manager, "opera")
            elif action == "brave":
                get_ddos_guard_cookies(manager, "brave")
            return

        # Enter Cookie Values Manually
        elif action == 2:
            bunkr_ddg1 = inquirer.text(
                message="请输入你的Bunkr用DDG1值:",
                default=manager.config_manager.authentication_data["DDOS-Guard"]["bunkrr_ddg1"],
            ).execute()
            bunkr_ddg2 = inquirer.text(
                message="请输入你的Bunkr用DDG2值:",
                default=manager.config_manager.authentication_data["DDOS-Guard"]["bunkrr_ddg2"],
            ).execute()
            bunkr_ddgid = inquirer.text(
                message="请输入你的Bunkr用DDGID值:",
                default=manager.config_manager.authentication_data["DDOS-Guard"]["bunkrr_ddgid"],
            ).execute()

            coomer_ddg1 = inquirer.text(
                message="请输入你的Coomer用DDG1值:",
                default=manager.config_manager.authentication_data["DDOS-Guard"]["coomer_ddg1"],
            ).execute()
            kemono_ddg1 = inquirer.text(
                message="请输入你的Kemono用DDG1值:",
                default=manager.config_manager.authentication_data["DDOS-Guard"]["kemono_ddg1"],
            ).execute()

            manager.config_manager.authentication_data["DDOS-Guard"]["bunkr_ddg1"] = bunkr_ddg1
            manager.config_manager.authentication_data["DDOS-Guard"]["bunkr_ddg2"] = bunkr_ddg2
            manager.config_manager.authentication_data["DDOS-Guard"]["bunkr_ddgid"] = bunkr_ddgid
            manager.config_manager.authentication_data["DDOS-Guard"]["coomer_ddg1"] = coomer_ddg1
            manager.config_manager.authentication_data["DDOS-Guard"]["kemono_ddg1"] = kemono_ddg1

            return
        elif action == 3:
            return


def edit_forum_authentication_values_prompt(manager: Manager) -> None:
    """Edit the forum authentication values"""
    while True:
        console.clear()
        console.print("编辑论坛认证值")
        action = inquirer.select(
            message="你想进行什么操作？",
            choices=[
                Choice(1, "浏览器Cookie提取"),
                Choice(2, "手动输入Cookie值"),
                Choice(3, "完成"),
            ], long_instruction="方向键: 导航 | 回车: 选择"
        ).execute()

        # Browser Cookie Extraction
        if action == 1:
            action = inquirer.select(
                message="我们应从哪个浏览器加载Cookie？",
                choices=[
                    Choice("chrome", "Chrome"),
                    Choice("firefox", "FireFox"),
                    Choice("edge", "Edge"),
                    Choice("safari", "Safari"),
                    Choice("opera", "Opera"),
                    Choice("brave", "Brave"),
                    Choice(1, "完成"),
                ], long_instruction="方向键: 导航 | 回车: 选择"
            ).execute()

            # Done
            if action == 1:
                continue

            # Browser Selection
            if action == "chrome":
                get_forum_cookies(manager, "chrome")
            elif action == "firefox":
                get_forum_cookies(manager, "firefox")
            elif action == "edge":
                get_forum_cookies(manager, "edge")
            elif action == "safari":
                get_forum_cookies(manager, "safari")
            elif action == "opera":
                get_forum_cookies(manager, "opera")
            elif action == "brave":
                get_forum_cookies(manager, "brave")
            return

        # Enter Cookie Values Manually
        elif action == 2:
            celebforum_username = inquirer.text(
                message="请输入你的CelebForum用户名:",
                default=manager.config_manager.authentication_data["Forums"]["celebforum_username"],
            ).execute()
            celebforum_password = inquirer.text(
                message="请输入你的CelebForum密码:",
                default=manager.config_manager.authentication_data["Forums"]["celebforum_password"],
            ).execute()

            f95zone_username = inquirer.text(
                message="请输入你的F95Zone用户名:",
                default=manager.config_manager.authentication_data["Forums"]["f95zone_username"],
            ).execute()
            f95zone_password = inquirer.text(
                message="请输入你的F95Zone密码:",
                default=manager.config_manager.authentication_data["Forums"]["f95zone_password"],
            ).execute()

            leakedmodels_username = inquirer.text(
                message="请输入你的LeakedModels用户名:",
                default=manager.config_manager.authentication_data["Forums"]["leakedmodels_username"],
            ).execute()
            leakedmodels_password = inquirer.text(
                message="请输入你的LeakedModels密码:",
                default=manager.config_manager.authentication_data["Forums"]["leakedmodels_password"],
            ).execute()

            nudostar_username = inquirer.text(
                message="请输入你的NudoStar用户名:",
                default=manager.config_manager.authentication_data["Forums"]["nudostar_username"],
            ).execute()
            nudostar_password = inquirer.text(
                message="请输入你的NudoStar密码:",
                default=manager.config_manager.authentication_data["Forums"]["nudostar_password"],
            ).execute()

            simpcity_username = inquirer.text(
                message="请输入你的SimpCity用户名:",
                default=manager.config_manager.authentication_data["Forums"]["simpcity_username"],
            ).execute()
            simpcity_password = inquirer.text(
                message="请输入你的SimpCity密码:",
                default=manager.config_manager.authentication_data["Forums"]["simpcity_password"],
            ).execute()

            socialmediagirls_username = inquirer.text(
                message="请输入你的SocialMediaGirls用户名:",
                default=manager.config_manager.authentication_data["Forums"]["socialmediagirls_username"],
            ).execute()
            socialmediagirls_password = inquirer.text(
                message="请输入你的SocialMediaGirls密码:",
                default=manager.config_manager.authentication_data["Forums"]["socialmediagirls_password"],
            ).execute()

            xbunker_username = inquirer.text(
                message="请输入你的XBunker用户名:",
                default=manager.config_manager.authentication_data["Forums"]["xbunker_username"],
            ).execute()
            xbunker_password = inquirer.text(
                message="请输入你的XBunker密码:",
                default=manager.config_manager.authentication_data["Forums"]["xbunker_password"],
            ).execute()

            manager.config_manager.authentication_data["Forums"]["celebforum_username"] = celebforum_username
            manager.config_manager.authentication_data["Forums"]["f95zone_username"] = f95zone_username
            manager.config_manager.authentication_data["Forums"]["leakedmodels_username"] = leakedmodels_username
            manager.config_manager.authentication_data["Forums"]["nudostar_username"] = nudostar_username
            manager.config_manager.authentication_data["Forums"]["simpcity_username"] = simpcity_username
            manager.config_manager.authentication_data["Forums"]["socialmediagirls_username"] = socialmediagirls_username
            manager.config_manager.authentication_data["Forums"]["xbunker_username"] = xbunker_username

            manager.config_manager.authentication_data["Forums"]["celebforum_password"] = celebforum_password
            manager.config_manager.authentication_data["Forums"]["f95zone_password"] = f95zone_password
            manager.config_manager.authentication_data["Forums"]["leakedmodels_password"] = leakedmodels_password
            manager.config_manager.authentication_data["Forums"]["nudostar_password"] = nudostar_password
            manager.config_manager.authentication_data["Forums"]["simpcity_password"] = simpcity_password
            manager.config_manager.authentication_data["Forums"]["socialmediagirls_password"] = socialmediagirls_password
            manager.config_manager.authentication_data["Forums"]["xbunker_password"] = xbunker_password
            return
        elif action == 3:
            return


def edit_jdownloader_authentication_values_prompt(auth: Dict) -> None:
    """编辑JDownloader的认证值"""
    console.clear()
    jdownloader_username = inquirer.text(
        message="请输入JDownloader用户名:",
        default=auth["JDownloader"]["jdownloader_username"],
    ).execute()
    jdownloader_password = inquirer.text(
        message="请输入JDownloader密码:",
        default=auth["JDownloader"]["jdownloader_password"],
    ).execute()
    jdownloader_device = inquirer.text(
        message="请输入JDownloader设备名称:",
        default=auth["JDownloader"]["jdownloader_device"],
    ).execute()

    auth["JDownloader"]["jdownloader_username"] = jdownloader_username
    auth["JDownloader"]["jdownloader_password"] = jdownloader_password
    auth["JDownloader"]["jdownloader_device"] = jdownloader_device


def edit_reddit_authentication_values_prompt(auth: Dict) -> None:
    """Edit the reddit authentication values"""
    console.clear()
    console.print(
        "你可以在这里创建一个Reddit应用来使用：https://www.reddit.com/prefs/apps/"
    )
    reddit_secret = inquirer.text(
        message="请输入Reddit密钥值:",
        default=auth["Reddit"]["reddit_secret"],
    ).execute()
    reddit_personal_use_script = inquirer.text(
        message="请输入Reddit个人用途脚本值:",
        default=auth["Reddit"]["reddit_personal_use_script"],
    ).execute()

    auth["Reddit"]["reddit_secret"] = reddit_secret
    auth["Reddit"]["reddit_personal_use_script"] = reddit_personal_use_script
