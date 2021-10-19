from src.render import RenderWindow
from src.sim import Simulation
from src.physics import Vector2D
from src.generations import RobotEvolver


if __name__ == "__main__":
    evolver = RobotEvolver(height=480, width=640)
    evolver.sim.add_robots(count=12)
    evolver.sim.set_robot_target(Vector2D(160, 120))
    for i in range(1000):
        evolver.run_generation(max_steps=150)
        best_score = min(robot.score for robot in evolver.sim.robots)
        print(f"Generation: {i} Best Score: {best_score}")
