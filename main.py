from src.render import RenderWindow
from src.sim import Simulation
from src.physics import Vector2D


if __name__ == "__main__":
    sim = Simulation(width=680, height=480)
    win: RenderWindow = RenderWindow(sim)

    sim.add_robots(10)
    sim.set_robot_target(Vector2D(600, 300))

    win.main_loop(1 / 60)
