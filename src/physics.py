from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt
import pygame as pg


@dataclass
class Vector2D:
    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __truediv__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x / scalar, self.y / scalar)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Vector2D) -> Vector2D:
        return other - self

    def __mul__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector2D:
        return self * scalar

    @property
    def length(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def reset(self) -> None:
        self.x, self.y = 0, 0


class RoundMass:

    pos: Vector2D
    vel: Vector2D
    acc: Vector2D

    def __init__(self):
        self.pos = Vector2D(0, 0)
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)

    def tick(self) -> None:
        self.vel += self.acc
        self.pos += self.vel
        self.acc.reset()

    def approach_target(self, target: Vector2D) -> None:
        dx = target.x - self.pos.x
        dy = target.y - self.pos.y
        self.acc = Vector2D(dx / 360, dy / 360)

    def apply_force(self, force: Vector2D) -> None:
        self.acc += force

    def apply_friction(self) -> None:
        mu = 1
        if self.vel.length < mu:
            self.vel.x, self.vel.y = 0, 0
        else:
            scale = (self.vel.length - mu) / self.vel.length
            self.vel.x *= scale
            self.vel.y *= scale
