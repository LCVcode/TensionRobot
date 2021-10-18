from __future__ import annotations
from src.physics import RoundMass, Vector2D


class TensionRobot:

    effector: RoundMass
    HEI: int
    WID: int
    POWER: float
    agent: Agent

    def __init__(
        self, width: int, height: int, power: float = 10, agent: Agent = None
    ):
        self.HEI, self.WID = height, width
        self.POWER = power
        self.effector = RoundMass(mass=3)
        self.agent = agent or Agent()
        self.reset()

    def reset(self) -> None:
        """Reset the TensionRobot to its inital state."""
        self.effector.pos.x = self.WID / 2
        self.effector.pos.y = self.HEI / 2
        self.effector.vel.reset()
        self.effector.acc.reset()
        self.effector.net_force.reset()

    def tick(self, inputs: tuple[float, float, float, float]) -> None:
        anchors = self.get_anchors()
        tension_vectors = tuple(
            (vec - self.effector.pos).normalize() for vec in anchors
        )
        forces = (
            strength * unit for strength, unit in zip(inputs, tension_vectors)
        )
        for force in forces:
            self.effector.apply_force(force)
        self.effector.tick()

    def get_anchors(self) -> tuple[Vector2D, Vector2D, Vector2D, Vector2D]:
        return (
            Vector2D(0, 0),
            Vector2D(self.WID, 0),
            Vector2D(0, self.HEI),
            Vector2D(self.WID, self.HEI),
        )


class Agent:
    pass
