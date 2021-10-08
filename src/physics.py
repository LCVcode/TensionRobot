from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame as pg


@dataclass
class Vector2D:
    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)


class RoundMass:

    pos: Vector2D
    vel: Vector2D
    acc: Vector2D

    def __init__(self):
        self.pos = Vector2D(0, 0)
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)

    def tick(self) -> None:
        x, y = pg.mouse.get_pos()
        self.approach_target(Vector2D(x, y))
        self.vel += self.acc
        self.pos += self.vel

    def approach_target(self, target: Vector2D) -> None:
        dx = target.x - self.pos.x
        dy = target.y - self.pos.y
        self.vel = Vector2D(dx / 30, dy / 30)
