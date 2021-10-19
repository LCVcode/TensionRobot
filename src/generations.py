from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from pygame.constants import RESIZABLE


from src.render import RenderWindow
from src.robot import Agent, TensionRobot
from src.sim import Simulation


class RobotEvolver:

    sim: Simulation
    win: RenderWindow
    breeder: Reproducer
    generation_count: int
    score_log: list[tuple[float, ...]]

    def __init__(self, width: int, height: int) -> None:
        self.sim = Simulation(height=height, width=width)
        self.win = RenderWindow(self.sim)
        self.breeder = GreedyAlphaReproducer(0.02)
        self.generation_count = 0
        self.score_log = []

    def run_epoch(self, max_steps: int, fps: int) -> None:
        """Runs a single epoch.
        Does not modify any data."""
        self.sim.reset()
        self.win.main_loop(fps=fps, frame_limit=max_steps)
        self.score_log.append(tuple(sorted(r.score for r in self.sim.robots)))

    def run_generation(self, max_steps: int, fps: int = 60) -> None:
        """Runs an epoch and produces the next generation."""
        # Score robots
        self.run_epoch(fps=fps, max_steps=max_steps)

        # Generate a new generation of Agents
        new_agents = self.breeder.next_generation(self.sim.robots)

        # Applies the new Agents
        for agent, robot in zip(new_agents, self.sim.robots):
            robot.agent = agent
        self.generation_count += 1

    def _rounds_without_improvements(self) -> int:
        rel_scores = self.relative_scores()
        if not len(rel_scores):
            return 0
        i = len(rel_scores) - 1
        while rel_scores[i] == 0:
            i -= 1
        return len(rel_scores) - i - 1

    def relative_scores(self) -> tuple[float, ...]:
        rel_scores: list[float] = [0 for _ in range(len(self.score_log) - 1)]
        for i in range(len(rel_scores)):
            rel_scores[i] = min(self.score_log[i]) - min(self.score_log[i + 1])
        return tuple(rel_scores)


class Reproducer(ABC):
    @abstractmethod
    def next_generation(self, robots: set[TensionRobot]) -> set[Agent]:
        pass

    def get_child(self, parent: Agent) -> Agent:
        pass


@dataclass
class GreedyAlphaReproducer(Reproducer):

    scale: float

    def next_generation(self, robots: set[TensionRobot]) -> set[Agent]:
        alpha = tuple(robots)[0]
        score = None
        for robot in robots:
            alpha = robot if score is None else alpha
            score = robot.score if score is None else score
            if robot.score < score:
                alpha, score = robot, robot.score

        next_generation = {alpha.agent}
        while len(next_generation) < len(robots):
            next_generation.add(self.get_child(alpha.agent))

        return next_generation

    def get_child(self, parent: Agent) -> Agent:
        """Simple stochastic asexual reproduction."""

        shape = parent.brain.shape
        overlay = np.random.random(shape) * (2 * self.scale) - self.scale

        child = Agent(parent.brain + overlay)
        return child
