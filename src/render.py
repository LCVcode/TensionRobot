from __future__ import annotations
import pygame as pg
import time
from typing import Callable, Union

from src.physics import RoundMass, Vector2D
from src.sim import Simulation
from src.robot import TensionRobot


# TODO:
# 1. Cleanup renderer draw methods (consolidate)


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
        return {
            RoundMass: self._draw_round_mass,
            TensionRobot: self._draw_robot,
        }

    def main_loop(self, fps: int = 30, frame_limit: int = 0):
        running: bool = True
        frame_counter: int = 0
        time_step = 1 / fps

        while running:
            t_start: float = time.time()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self._SIM.tick()
            self.draw_all()
            frame_counter += 1
            if frame_limit and frame_limit < frame_counter:
                running = False
            while time.time() - t_start < time_step:
                pass

    def draw_all(self) -> None:
        self._DISPLAY.fill((0, 0, 0))
        self.draw_entites()
        self.draw_robots()
        pg.display.flip()

    def draw_line_to_mouse(self) -> None:
        pg.draw.line(self._DISPLAY, (0, 210, 160), (0, 0), pg.mouse.get_pos())

    def draw_entites(self) -> None:
        for entity in self._SIM.entities:
            self._draw_entity(entity)

    def draw_robots(self) -> None:
        for robot in self._SIM.robots:
            self._draw_entity(robot)

    def _draw_entity(self, entity: Union[RoundMass, TensionRobot]) -> None:
        if type(entity) in self._MAP:
            self._MAP[type(entity)](entity)
        else:
            raise TypeError(f"Cannot render {type(entity)}.")

    def _draw_round_mass(self, mass: RoundMass) -> None:
        self._draw_point(mass.pos, color=(210, 210, 210))

    def _draw_point(
        self, point: Vector2D, color: tuple[int, int, int] = (210, 210, 210)
    ) -> None:
        pg.draw.circle(self._DISPLAY, color, (point.x, point.y), 5)

    def _draw_robot(self, robot: TensionRobot) -> None:
        for anchor in robot.get_anchors():
            pg.draw.line(
                self._DISPLAY,
                (50, 50, 50),
                anchor.to_tuple(),
                robot.effector.pos.to_tuple(),
            )
        self._draw_round_mass(robot.effector)
        self._draw_point(robot.target, color=(10, 210, 233))
