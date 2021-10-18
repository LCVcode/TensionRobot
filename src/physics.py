from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import FrozenInstanceError, dataclass
from math import sqrt
import pygame as pg

G = 9.8


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

    def normalize(self) -> Vector2D:
        length = self.length
        return Vector2D(self.x / length, self.y / length)

    @property
    def length(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def reset(self) -> None:
        self.x, self.y = 0, 0


class RoundMass:

    _MU_STATIC: float = 0.006
    _MU_SLIDING: float = 0.005

    pos: Vector2D
    vel: Vector2D
    acc: Vector2D
    net_force: Vector2D
    mass: float

    def __init__(self, mass: float = 1):
        self.pos = Vector2D(0, 0)
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)
        self.net_force = Vector2D(0, 0)
        self.mass = mass

    def tick(self) -> None:
        self.acc = self.net_force / self.mass
        self.vel += self.acc
        self.pos += self.vel
        self.net_force.reset()

    def approach_target(self, target: Vector2D) -> None:
        dx = target.x - self.pos.x
        dy = target.y - self.pos.y
        self.acc = Vector2D(dx / 360, dy / 360)

    def apply_force(self, force: Vector2D) -> None:
        self.net_force += force
        # self.acc += force / self.mass

    def apply_friction(self) -> None:
        if not self.vel.length:
            self._apply_static_friction()
        else:
            self._apply_sliding_friction()

    def _apply_static_friction(self) -> None:
        magnitude: float = G * self.mass * self._MU_STATIC
        length = self.net_force.length

        if length < magnitude:
            # Static friction overcomes net_force
            self.net_force.reset()
        else:
            # Net_force overcomes static friction
            self.net_force *= (length - magnitude) / length

    def _apply_sliding_friction(self) -> None:
        magnitude: float = G * self.mass * self._MU_SLIDING

        friction = self.vel * (-magnitude / self.vel.length)
        if friction.length > self.vel.length * self.mass:
            self.vel.reset()
            self.net_force.reset()
            return
        self.apply_force(friction)
