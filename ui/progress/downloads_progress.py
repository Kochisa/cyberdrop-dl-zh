from typing import Tuple

from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn


class DownloadsProgress:
    """用于跟踪已完成、已跳过和失败文件的类"""

    def __init__(self):
        self.progress = Progress("[progress.description]{task.description}",
                                 BarColumn(bar_width=None),
                                 "[progress.percentage]{task.percentage:>3.2f}%",
                                 "{task.completed} of {task.total} 个文件")
        self.progress_group = Group(self.progress)

        self.total_files = 0
        self.completed_files_task_id = self.progress.add_task("[green]已完成", total=0)
        self.completed_files = 0
        self.previously_completed_files_task_id = self.progress.add_task("[yellow]之前已下载", total=0)
        self.previously_completed_files = 0
        self.skipped_files_task_id = self.progress.add_task("[yellow]根据配置跳过", total=0)
        self.skipped_files = 0
        self.failed_files_task_id = self.progress.add_task("[red]失败", total=0)
        self.failed_files = 0

    async def get_progress(self) -> Panel:
        """返回进度条"""
        return Panel(self.progress_group, title="文件", border_style="green", padding=(1, 1))

    async def update_total(self) -> None:
        """更新要下载的文件总数"""
        self.total_files = self.total_files + 1
        self.progress.update(self.completed_files_task_id, total=self.total_files)
        self.progress.update(self.previously_completed_files_task_id, total=self.total_files)
        self.progress.update(self.skipped_files_task_id, total=self.total_files)
        self.progress.update(self.failed_files_task_id, total=self.total_files)

    async def add_completed(self) -> None:
        """将已完成的文件添加到进度条"""
        self.progress.advance(self.completed_files_task_id, 1)
        self.completed_files += 1

    async def add_previously_completed(self, increase_total: bool = True) -> None:
        """将以前已完成的文件添加到进度条"""
        if increase_total:
            await self.update_total()
        self.previously_completed_files += 1
        self.progress.advance(self.previously_completed_files_task_id, 1)

    async def add_skipped(self) -> None:
        """将跳过的文件添加到进度条"""
        self.progress.advance(self.skipped_files_task_id, 1)
        self.skipped_files += 1

    async def add_failed(self) -> None:
        """将失败的文件添加到进度条"""
        self.progress.advance(self.failed_files_task_id, 1)
        self.failed_files += 1

    async def return_totals(self) -> Tuple[int, int, int, int]:
        """返回已完成、之前已完成、已跳过和失败文件的总数"""
        return self.completed_files, self.previously_completed_files, self.skipped_files, self.failed_files
