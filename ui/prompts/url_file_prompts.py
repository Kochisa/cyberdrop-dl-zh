import re
from pathlib import Path

from InquirerPy import inquirer
from rich.console import Console

console = Console()

def edit_urls_prompt(URLs_File: Path, fix_strings=True) -> None:
    """
    编辑 URL 文件的功能函数。
    
    参数:
    - URLs_File: Path 类型，指定需要编辑的 URL 文件的路径。
    - fix_strings: 布尔类型，默认为 True，当为 True 时，会自动将连续的空格替换为换行符，并移除多余的换行符。
    
    返回值:
    - 无返回值。
    """
    console.clear()  # 清除控制台内容
    console.print(f"编辑 URL: {URLs_File}")  # 打印编辑的文件名

    # 读取现有 URL 文件的内容
    with open(URLs_File, "r") as f:
        existing_urls = f.read()

    # 使用 InquirerPy 库进行文本输入，允许用户编辑 URL
    result = inquirer.text(
        message="URLs:", multiline=True, default=existing_urls,
        long_instruction="按下 Escape 然后回车键完成编辑。",
    ).execute()

    # 如果启用字符串修正，则进行空格到换行符的替换及多余换行符的移除
    if fix_strings:
        result = result.replace(" ", "\n")
        result = re.sub(r"(\n)+", "\n", result)  # 移除多余的换行符

    # 写入编辑后的内容到文件
    with open(URLs_File, "w") as f:
        f.write(result)
