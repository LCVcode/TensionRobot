from src.render import RenderWindow
from src.sim import Simulation
from src.physics import RoundMass


if __name__ == "__main__":
    sim = Simulation(width=480, height=360)
    win: RenderWindow = RenderWindow(sim)
    mass: RoundMass = RoundMass()
    sim.add_mass(mass)
    win.main_loop(1 / 60)
