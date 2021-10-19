from src.render import RenderWindow
from src.sim import Simulation
from src.physics import Vector2D
from src.generations import RobotEvolver


if __name__ == "__main__":
    evolver = RobotEvolver(height=680, width=1440)
    evolver.sim.add_robots(count=12)
    evolver.sim.set_robot_target(Vector2D(740, 340))
    for i in range(1000):
        evolver.run_generation(max_steps=240, fps=0)
        best_score = round(min(robot.score for robot in evolver.sim.robots), 3)
        print(
            f"Generation: {i} Best Score: {best_score} Stagnation: {evolver._rounds_without_improvements()}"
        )
