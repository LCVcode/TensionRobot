import pygame as pg
import time
from typing import Callable

from src.physics import RoundMass
from src.sim import Simulation


class RenderWindow:

    HEIGHT: int
    WIDTH: int
    _DISPLAY: pg.surface.Surface
    _SIM: Simulation
    _MAP: dict[type, Callable]

    def __init__(self, sim: Simulation):
        self._SIM = sim
        self._DISPLAY = pg.display.set_mode((sim.WIDTH, sim.HEIGHT))
        self._MAP = self.__draw_call_mapping()

    def __draw_call_mapping(self) -> dict[type, Callable]:
        return {RoundMass: self._draw_round_mass}

    def main_loop(self, time_step: float = 0):
        running: bool = True

        while running:
            t_start: float = time.time()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self._SIM.tick()
            self.draw_all()
            while time.time() - t_start < time_step:
                pass

    def draw_all(self) -> None:
        self._DISPLAY.fill((0, 0, 0))
        pg.draw.circle(self._DISPLAY, (120, 30, 0), (0, 0), 50)
        self.draw_entites()
        self.draw_line_to_mouse()
        pg.display.flip()

    def draw_line_to_mouse(self) -> None:
        pg.draw.line(self._DISPLAY, (0, 210, 160), (0, 0), pg.mouse.get_pos())

    def draw_entites(self) -> None:
        for entity in self._SIM.entities:
            if type(entity) in self._MAP:
                self._MAP[type(entity)](entity)
            else:
                raise TypeError(f"Cannot render {type(entity)}.")

    def _draw_round_mass(self, mass: RoundMass) -> None:
        color = (210, 210, 210)
        pg.draw.circle(self._DISPLAY, color, (mass.pos.x, mass.pos.y), 5)
