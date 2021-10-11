from src.render import RenderWindow
from src.sim import Simulation
from src.physics import RoundMass


if __name__ == "__main__":
    sim = Simulation(width=480, height=360)
    win: RenderWindow = RenderWindow(sim)
    mass: RoundMass = RoundMass()
    mass.pos.x = 450
    mass.pos.y = 250
    sim.add_mass(mass)
    sim.add_mass(RoundMass())
    win.main_loop(1 / 60)
