from src.render import RenderWindow


if __name__ == "__main__":
    win: RenderWindow = RenderWindow(480, 330)
    win.main_loop(0.03)
