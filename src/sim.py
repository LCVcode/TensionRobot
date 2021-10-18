from src.physics import RoundMass, Vector2D
from src.robot import TensionRobot


class Simulation:

    HEIGHT: int
    WIDTH: int
    entities: set[RoundMass]
    robots: set[TensionRobot]

    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.entities = set()
        self.robots = set()

    def add_mass(self, mass: RoundMass) -> None:
        self.entities.add(mass)

    def add_robot(self, robot: TensionRobot) -> None:
        self.robots.add(robot)

    def tick(self) -> None:
        for entity in self.entities:
            entity.tick()

        for robot in self.robots:
            robot.tick()

    def add_robots(self, count: int, power: float = 10):
        for _ in range(count):
            self.add_robot(
                TensionRobot(width=self.WIDTH, height=self.HEIGHT, power=power)
            )

    def set_robot_target(self, target: Vector2D) -> None:
        for robot in self.robots:
            robot.set_target(target)
