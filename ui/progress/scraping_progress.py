from typing import List, TYPE_CHECKING

from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TaskID
from yarl import URL

if TYPE_CHECKING:
    from cyberdrop_dl.managers.manager import Manager


async def adjust_title(s: str, length: int = 40, placeholder: str = "...") -> str:
    """折叠、截断或填充给定的字符串，以适应给定的长度"""
    return f"{s[:length - len(placeholder)]}{placeholder}" if len(s) >= length else s.ljust(length)


class ScrapingProgress:
    """管理单个文件下载进度的类"""
    def __init__(self, visible_tasks_limit: int, manager: 'Manager'):
        self.manager = manager

        self.progress = Progress(SpinnerColumn(),
                                 "[progress.description]{task.description}")
        self.overflow = Progress("[progress.description]{task.description}")
        self.queue = Progress("[progress.description]{task.description}")
        self.progress_group = Group(self.progress, self.overflow, self.queue)

        self.color = "plum3"
        self.type_str = "链接"
        self.progress_str = "[{color}]{description}"
        self.overflow_str = "[{color}]... 和其他链接数量: {number}"
        self.queue_str = "[{color}]... 和抓取队列中的链接数量: {number}"
        self.overflow_task_id = self.overflow.add_task(self.overflow_str.format(color=self.color, number=0, type_str=self.type_str), visible=False)
        self.queue_task_id = self.queue.add_task(self.queue_str.format(color=self.color, number=0, type_str=self.type_str), visible=False)

        self.visible_tasks: List[TaskID] = []
        self.invisible_tasks: List[TaskID] = []
        self.tasks_visibility_limit = visible_tasks_limit

    async def get_progress(self) -> Panel:
        """返回进度条"""
        return Panel(self.progress_group, title="抓取", border_style="green", padding=(1, 1))

    async def get_queue_length(self) -> int:
        """返回抓取器队列中的任务数量"""
        total = 0

        total += self.manager.queue_manager.url_objects_to_map.qsize()
        for queue in self.manager.queue_manager.scraper_queues.values():
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

    async def add_task(self, url: URL) -> TaskID:
        """向进度条添加新任务"""
        if len(self.visible_tasks) >= self.tasks_visibility_limit:
            task_id = self.progress.add_task(self.progress_str.format(color=self.color, description=str(url)), visible=False)
            self.invisible_tasks.append(task_id)
        else:
            task_id = self.progress.add_task(self.progress_str.format(color=self.color, description=str(url)))
            self.visible_tasks.append(task_id)
        return task_id

    async def remove_task(self, task_id: TaskID) -> None:
        """从进度条中移除任务"""
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
