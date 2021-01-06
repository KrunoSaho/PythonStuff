from dataclasses import dataclass
from enum import Enum
import random


class TaskType(Enum):
    IDLE = 0
    GATHER = 1
    ACTIVITY = 2


@dataclass(unsafe_hash=True)
class Task:
    name: str
    type: TaskType
    time_to_complete: float = 0.0


class TaskManager:
    ids: list[int]
    unassigned_tasks = list[int]
    assigned_tasks: dict[int, Task]

    def __init__(self, ids: list[int]) -> None:
        super().__init__()
        self.ids = ids[::]
        self.unassigned_tasks = ids[::]
        self.assigned_tasks = {}

    def randomly_assign(self, tasks_to_assign: list[Task]):
        unassigned = self.unassigned_tasks
        ids = random.choices(unassigned, k=len(tasks_to_assign))  # type: ignore
        tasks = {i: t for i, t in zip(ids, tasks_to_assign)}
        self.unassigned_tasks = list(set(self.unassigned_tasks) - set(ids))  # type: ignore
        self.assigned_tasks = tasks