from typing import Dict

from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TaskID


class DownloadStatsProgress:
    """记录下载失败和失败原因的类"""

    def __init__(self):
        self.progress = Progress("[progress.description]{task.description}",
                                 BarColumn(bar_width=None),
                                 "[progress.percentage]{task.percentage:>3.2f}%",
                                 "{task.completed} of {task.total} Files")
        self.progress_group = Group(self.progress)

        self.failure_types: Dict[str, TaskID] = {}
        self.failed_files = 0

    async def get_progress(self) -> Panel:
        """返回进度条"""
        return Panel(self.progress_group, title="下载失败", border_style="green", padding=(1, 1))

    async def update_total(self, total: int) -> None:
        """更新需要下载的文件总数"""
        for key in self.failure_types:
            self.progress.update(self.failure_types[key], total=total)

    async def add_failure(self, failure_type: [str, int]) -> None:
        """向进度条添加一个下载失败的文件"""
        self.failed_files += 1
        if isinstance(failure_type, int):
            failure_type = str(failure_type) + " HTTP 状态"

        if failure_type in self.failure_types:
            self.progress.advance(self.failure_types[failure_type], 1)
        else:
            self.failure_types[failure_type] = self.progress.add_task(failure_type, total=self.failed_files, completed=1)
        await self.update_total(self.failed_files)

    async def return_totals(self) -> Dict:
        """返回下载失败的文件总数"""
        failures = {}
        for key, value in self.failure_types.items():
            failures[key] = self.progress.tasks[value].completed
        return failures


class ScrapeStatsProgress:
    """记录抓取失败和失败原因的类"""

    def __init__(self):
        self.progress = Progress("[progress.description]{task.description}",
                                 BarColumn(bar_width=None),
                                 "[progress.percentage]{task.percentage:>3.2f}%",
                                 "{task.completed} of {task.total} Files")
        self.progress_group = Group(self.progress)

        self.failure_types: Dict[str, TaskID] = {}
        self.failed_files = 0

    async def get_progress(self) -> Panel:
        """返回进度条"""
        return Panel(self.progress_group, title="抓取失败", border_style="green", padding=(1, 1))

    async def update_total(self, total: int) -> None:
        """更新需要抓取的站点总数"""
        for key in self.failure_types:
            self.progress.update(self.failure_types[key], total=total)

    async def add_failure(self, failure_type: [str, int]) -> None:
        """向进度条添加一个抓取失败的站点"""
        self.failed_files += 1
        if isinstance(failure_type, int):
            failure_type = str(failure_type) + " HTTP 状态"

        if failure_type in self.failure_types:
            self.progress.advance(self.failure_types[failure_type], 1)
        else:
            self.failure_types[failure_type] = self.progress.add_task(failure_type, total=self.failed_files, completed=1)
        await self.update_total(self.failed_files)

    async def return_totals(self) -> Dict:
        """返回抓取失败的站点总数和失败原因"""
        failures = {}
        for key, value in self.failure_types.items():
            failures[key] = self.progress.tasks[value].completed
        return failures
