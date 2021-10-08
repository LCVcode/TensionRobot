from src.physics import RoundMass


class Simulation:

    HEIGHT: int
    WIDTH: int
    entities: set[RoundMass]

    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.entities = set()

    def add_mass(self, mass: RoundMass) -> None:
        self.entities.add(mass)

    def tick(self) -> None:
        for entity in self.entities:
            entity.tick()
