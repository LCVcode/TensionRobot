from __future__ import annotations
import numpy as np
import numpy.typing as npt
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

    # def tick(self, inputs: tuple[float, float, float, float]) -> None:
    def tick(self, target: Vector2D) -> None:
        anchors = self.get_anchors()
        tension_vectors = tuple(
            (vec - self.effector.pos).normalize() for vec in anchors
        )
        inputs = self.agent.get_inputs(target, self.effector)
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
    brain: npt.NDArray[np.float64]

    def __init__(self) -> None:
        self.brain = np.random.random((6, 4)) * 2 - 1

    def get_inputs(
        self, target: Vector2D, effector: RoundMass
    ) -> tuple[float, ...]:
        offset = target - effector.pos

        input_vector = np.zeros((1, 6))
        input_vector[0][0] = offset.x
        input_vector[0][1] = offset.y
        input_vector[0][2] = effector.pos.x
        input_vector[0][3] = effector.pos.y
        input_vector[0][4] = effector.vel.x
        input_vector[0][5] = effector.vel.y

        output_vector = input_vector.dot(self.brain)

        return tuple(Agent.sigmoid(x) for x in output_vector[0])

    @classmethod
    def sigmoid(cls, x: float) -> float:
        return 1 / (1 + np.exp(-x))
