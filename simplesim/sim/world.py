from dataclasses import dataclass
from typing import Optional
from entity import Entity, EntityManager, Point
from sim.taskmanager import Task, TaskManager
from renderer import Renderer
import events


@dataclass
class Resource:
    name: str
    value: int
    coords: Point


@dataclass
class EntityResource:
    entity: Entity
    resource: Resource


@dataclass
class EntityDelta:
    entity: Entity
    delta: Point


@dataclass
class Terrain:
    resources: list[Resource]

    def find(self, task: Task) -> Optional[Resource]:
        res = [r for r in self.resources if task.name == r.name]
        return res[0] if len(res) > 0 else None


@dataclass
class World:
    terrain: Terrain
    entity_manager: EntityManager
    task_manager: TaskManager

    def get_task_data(self) -> list[EntityResource]:
        tasks = self.task_manager.assigned_tasks
        entities = self.entity_manager.entities
        assigned_ids = tasks.keys()
        task_runners = [(e, tasks[e.id]) for e in entities if e.id in assigned_ids]
        # find task targets
        res = None
        return [
            EntityResource(e, res)
            for e, t in task_runners
            if (res := self.terrain.find(t)) is not None
        ]

    def process_paths(self, entity_resource: list[EntityResource]) -> list[EntityDelta]:
        paths = [
            EntityDelta(er.entity, er.entity.coords.delta(er.resource.coords))
            for er in entity_resource
        ]
        return paths

    def process_events(self, entity_deltas: list[EntityDelta]):
        for entity_delta in entity_deltas:
            entity, delta = entity_delta.entity, entity_delta.delta
            new_coords = entity.coords + delta
            other_entity = self.entity_manager.find(new_coords)
            if other_entity:
                yield events.Event(entity, other_entity, events.EventType.DAMAGE)
            yield events.Event(entity, None, events.EventType.MOVE)


def run(world: World, renderer: Renderer, event_processor):
    entity_resource = world.get_task_data()
    entity_deltas = world.process_paths(entity_resource)
    for event in world.process_events(entity_deltas):
        if event.type == events.EventType.MOVE:
            renderer.parse_event(event)
        event_processor.process(event)
