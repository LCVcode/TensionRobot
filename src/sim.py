from src.physics import RoundMass, Vector2D
from src.robot import TensionRobot

import pygame as pg


class Simulation:

    HEIGHT: int
    WIDTH: int
    entities: set[RoundMass]
    robot: TensionRobot

    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.entities = set()
        self.robot = TensionRobot(width=width, height=height, power=10)

    def add_mass(self, mass: RoundMass) -> None:
        self.entities.add(mass)

    def tick(self) -> None:
        mouse_vec = Vector2D(*pg.mouse.get_pos())
        for entity in self.entities:
            entity.apply_force((mouse_vec - entity.pos) / 60)
            entity.apply_friction()

        for entity in self.entities:
            entity.tick()

        self.robot.tick((1, 1, 0.1, 0.9))
