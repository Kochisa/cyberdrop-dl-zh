import re
from pathlib import Path

from InquirerPy import inquirer
from rich.console import Console

console = Console()


def edit_urls_prompt(URLs_File: Path, fix_strings=True) -> None:
    """编辑 URL 文件"""
    console.clear()
    console.print(f"编辑 URL: {URLs_File}")
    with open(URLs_File, "r") as f:
        existing_urls = f.read()

    result = inquirer.text(
        message="URLs:", multiline=True, default=existing_urls,
        long_instruction="按下 Escape 然后回车键完成编辑。",
    ).execute()

    if fix_strings:
        result = result.replace(" ", "\n")
        result = re.sub(r"(\n)+", "\n", result)

    with open(URLs_File, "w") as f:
        f.write(result)
