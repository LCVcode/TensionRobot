from __future__ import annotations

from src.physics import RoundMass, Vector2D
from src.robot import TensionRobot, Agent

from abc import ABC, abstractmethod


class Simulation:

    HEIGHT: int
    WIDTH: int
    entities: set[RoundMass]
    robots: set[TensionRobot]
    metric: ScoringMetric

    def __init__(self, height: int, width: int, metric: ScoringMetric = None):
        self.HEIGHT = height
        self.WIDTH = width
        self.entities = set()
        self.robots = set()
        self.metric = metric or ManhattanDistanceMetric()

    def add_mass(self, mass: RoundMass) -> None:
        self.entities.add(mass)

    def add_robot(self, robot: TensionRobot) -> None:
        self.robots.add(robot)

    def tick(self) -> None:
        for entity in self.entities:
            entity.tick()

        for robot in self.robots:
            robot.tick()
            self.score(robot)

    def add_robots(self, count: int, power: float = 10):
        for _ in range(count):
            self.add_robot(
                TensionRobot(width=self.WIDTH, height=self.HEIGHT, power=power)
            )

    def set_robot_target(self, target: Vector2D) -> None:
        for robot in self.robots:
            robot.set_target(target)

    def reset(self) -> None:
        for robot in self.robots:
            robot.reset()

    def score(self, robot: TensionRobot) -> None:
        if robot.crashed:
            loss = self.metric.worst_case(self)
        else:
            loss = self.metric.evaluate(robot)
        robot.score += loss


class ScoringMetric(ABC):
    @abstractmethod
    def evaluate(self, robot: TensionRobot) -> float:
        pass

    def worst_case(self, sim: Simulation) -> float:
        pass


class ManhattanDistanceMetric(ScoringMetric):
    def evaluate(self, robot: TensionRobot) -> float:
        offset = robot.target - robot.effector.pos
        return abs(offset.x) + abs(offset.y)

    def worst_case(self, sim: Simulation) -> float:
        return sim.WIDTH + sim.HEIGHT
