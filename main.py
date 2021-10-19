from src.render import RenderWindow
from src.sim import Simulation
from src.physics import Vector2D
from src.generations import RobotEvolver


if __name__ == "__main__":
    evolver = RobotEvolver(height=880, width=1640)
    evolver.sim.add_robots(count=60)
    evolver.sim.set_robot_target(Vector2D(240, 440))
    for i in range(1000):
        evolver.run_generation(max_steps=270)
        best_score = round(min(robot.score for robot in evolver.sim.robots), 3)
        print(f"Generation: {i} Best Score: {best_score}")
