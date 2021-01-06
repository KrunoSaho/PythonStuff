from dataclasses import dataclass
from enum import Enum
from typing import Optional
import sim.world


class EventType(Enum):
    DAMAGE = 0
    MOVE = 1


@dataclass
class Event:
    src: sim.world.Entity
    dst: Optional[sim.world.Entity]
    type: EventType


class EventProcessor:
    def process(self, event: Event):
        if event.type == EventType.MOVE:
            pass