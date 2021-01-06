from events import EventProcessor
import os
from renderer import Renderer
import time
from util import timeit
from rich import print
import entity
import util
import sim.taskmanager
import sim.world


def run():
    # entities
    entity_manager = entity.EntityManager()

    entity_manager.generate_random(10000)
    entity_manager.set_dimension_values([(2, 0)])

    # tasks
    task_manager = sim.taskmanager.TaskManager(entity_manager.get_ids())
    tasks = [
        sim.taskmanager.Task("Hunt", sim.taskmanager.TaskType.GATHER),
        sim.taskmanager.Task("Cook", sim.taskmanager.TaskType.ACTIVITY),
        sim.taskmanager.Task("Clean", sim.taskmanager.TaskType.ACTIVITY),
        sim.taskmanager.Task("Gather Water", sim.taskmanager.TaskType.GATHER),
    ]
    task_manager.randomly_assign(tasks)

    # terrain
    terrain = sim.world.Terrain(
        [
            sim.world.Resource("Hunt", 2, entity.Point(-55, -33, 0)),
            sim.world.Resource("Cook", 4, entity.Point(15, 25, 0)),
            sim.world.Resource("Clean", 2, entity.Point(0, 0, 0)),
            sim.world.Resource("Gather Water", 100, entity.Point(5, 5, 0)),
        ]
    )

    # renderer
    renderer = Renderer()
    event_processor = EventProcessor()

    # run sim
    world = sim.world.World(terrain, entity_manager, task_manager)
    while True:
        sim.world.run(world, renderer, event_processor)
        time.sleep(0.16)


if __name__ == "__main__":
    os.system("cls")
    time_ran = util.timeit(run)
    print(f"Runtime: [bold green]{time_ran} [red]seconds")
