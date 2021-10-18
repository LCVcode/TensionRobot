from src.render import RenderWindow
from src.sim import Simulation
from src.physics import RoundMass, Vector2D
from src.robot import TensionRobot


if __name__ == "__main__":
    sim = Simulation(width=680, height=480)
    win: RenderWindow = RenderWindow(sim)

    sim.add_robots(10)

    win.main_loop(1 / 60)
