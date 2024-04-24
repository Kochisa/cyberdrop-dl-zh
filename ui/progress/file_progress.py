from typing import List, Optional, TYPE_CHECKING

from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, \
    TaskID

if TYPE_CHECKING:
    from cyberdrop_dl.managers.manager import Manager


async def adjust_title(s: str, length: int = 40, placeholder: str = "...") -> str:
    """折叠、截断或填充给定的字符串，以适应给定的长度"""
    return f"{s[:length - len(placeholder)]}{placeholder}" if len(s) >= length else s.ljust(length)


class FileProgress:
    """管理单个文件下载进度的类"""
    def __init__(self, visible_tasks_limit: int, manager: 'Manager'):
        self.manager = manager

        self.progress = Progress(SpinnerColumn(),
                                 "[progress.description]{task.description}",
                                 BarColumn(bar_width=None),
                                 "[progress.percentage]{task.percentage:>3.2f}%",
                                 "━",
                                 DownloadColumn(),
                                 "━",
                                 TransferSpeedColumn(),
                                 "━",
                                 TimeRemainingColumn())
        self.overflow = Progress("[progress.description]{task.description}")
        self.queue = Progress("[progress.description]{task.description}")
        self.progress_group = Group(self.progress, self.overflow, self.queue)

        self.color = "plum3"
        self.type_str = "文件"
        self.progress_str = "[{color}]{description}"
        self.overflow_str = "[{color}]... 和其他 {type_str} 数量: {number}"
        self.queue_str = "[{color}]... 和下载队列中的 {type_str} 数量: {number}"
        self.overflow_task_id = self.overflow.add_task(self.overflow_str.format(color=self.color, number=0, type_str=self.type_str), visible=False)
        self.queue_task_id = self.queue.add_task(self.queue_str.format(color=self.color, number=0, type_str=self.type_str), visible=False)

        self.visible_tasks: List[TaskID] = []
        self.invisible_tasks: List[TaskID] = []
        self.completed_tasks: List[TaskID] = []
        self.uninitiated_tasks: List[TaskID] = []
        self.tasks_visibility_limit = visible_tasks_limit

    async def get_progress(self) -> Panel:
        """返回进度条"""
        return Panel(self.progress_group, title="下载", border_style="green", padding=(1, 1))

    async def get_queue_length(self) -> int:
        """返回下载队列中的任务数量"""
        total = 0

        for queue in self.manager.queue_manager.download_queues.values():
            total += queue.qsize()

        return total

    async def redraw(self) -> None:
        """重新绘制进度条"""
        while len(self.visible_tasks) > self.tasks_visibility_limit:
            task_id = self.visible_tasks.pop(0)
            self.invisible_tasks.append(task_id)
            self.progress.update(task_id, visible=False)
        while len(self.invisible_tasks) > 0 and len(self.visible_tasks) < self.tasks_visibility_limit:
            task_id = self.invisible_tasks.pop(0)
            self.visible_tasks.append(task_id)
            self.progress.update(task_id, visible=True)

        if len(self.invisible_tasks) > 0:
            self.overflow.update(self.overflow_task_id, description=self.overflow_str.format(color=self.color, number=len(self.invisible_tasks), type_str=self.type_str), visible=True)
        else:
            self.overflow.update(self.overflow_task_id, visible=False)

        queue_length = await self.get_queue_length()
        if queue_length > 0:
            self.queue.update(self.queue_task_id, description=self.queue_str.format(color=self.color, number=queue_length, type_str=self.type_str), visible=True)
        else:
            self.queue.update(self.queue_task_id, visible=False)

    async def add_task(self, file: str, expected_size: Optional[int]) -> TaskID:
        """向进度条添加新任务"""
        description = file.split('/')[-1]
        description = description.encode("ascii", "ignore").decode().strip()
        description = await adjust_title(description)

        if len(self.visible_tasks) >= self.tasks_visibility_limit:
            task_id = self.progress.add_task(self.progress_str.format(color=self.color, description=description), total=expected_size, visible=False)
            self.invisible_tasks.append(task_id)
        else:
            task_id = self.progress.add_task(self.progress_str.format(color=self.color, description=description), total=expected_size)
            self.visible_tasks.append(task_id)
        return task_id

    async def remove_file(self, task_id: TaskID) -> None:
        """从进度条中移除给定的任务"""
        if task_id in self.visible_tasks:
            self.visible_tasks.remove(task_id)
            self.progress.update(task_id, visible=False)
        elif task_id in self.invisible_tasks:
            self.invisible_tasks.remove(task_id)
        elif task_id == self.overflow_task_id:
            self.overflow.update(task_id, visible=False)
        else:
            raise ValueError("找不到任务ID")
        await self.redraw()

    async def mark_task_completed(self, task_id: TaskID) -> None:
        """将给定的任务标记为已完成"""
        self.progress.update(task_id, visible=False)
        if task_id in self.visible_tasks:
            self.visible_tasks.remove(task_id)
        elif task_id in self.invisible_tasks:
            self.invisible_tasks.remove(task_id)
        await self.redraw()
        self.completed_tasks.append(task_id)

    async def advance_file(self, task_id: TaskID, amount: int) -> None:
        """以给定的数量推进给定任务的进度"""
        if task_id in self.uninitiated_tasks:
            self.uninitiated_tasks.remove(task_id)
            self.invisible_tasks.append(task_id)
            await self.redraw()
        self.progress.advance(task_id, amount)

    async def update_file_length(self, task_id: TaskID, total: int) -> None:
        """更新给定任务的待下载字节总数"""
        if task_id in self.invisible_tasks:
            self.progress.update(task_id, total=total, visible=False)
        elif task_id in self.visible_tasks:
            self.progress.update(task_id, total=total, visible=True)
        elif task_id in self.uninitiated_tasks:
            self.progress.update(task_id, total=total, visible=False)
            self.uninitiated_tasks.remove(task_id)
            self.invisible_tasks.append(task_id)
            await self.redraw()
