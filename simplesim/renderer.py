import random
import sys
import pygame
from pygame import gfxdraw
from enum import Enum
import events


class DrawEntity(Enum):
    POINT = 0


def pygame_init():
    pygame.init()

    size = 1280, 720
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    prior_draws = []

    iterations = 0

    while True:
        if iterations > 10_000:
            prior_draws.clear()
        (draw_entity, data) = yield

        #  rendering
        if draw_entity == DrawEntity.POINT:
            x, y = data.x, data.y
            sx = (x + 100) * 5
            sy = (y + 100) * 5
            draw_fn = lambda xx, yy: lambda: gfxdraw.circle(
                screen, xx, yy, 2, (255, 255, 255)
            )
            prior_draws.append(draw_fn(sx, sy))

        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # idle time
        screen.fill(black)
        for fn in prior_draws:
            fn()
        pygame.display.flip()
        iterations += 1


class Renderer:
    def __init__(self) -> None:
        super().__init__()
        self.render = pygame_init()
        self.render.send(None)

    def parse_event(self, event):
        if event.type == events.EventType.MOVE:
            data = (DrawEntity.POINT, event.src.coords)
            self.render.send(data)  # type: ignore
