import pygame as pg
import time


class RenderWindow:

    HEIGHT: int
    WIDTH: int
    _DISPLAY: pg.surface.Surface

    def __init__(self, width: int, height: int):
        self._DISPLAY = pg.display.set_mode((width, height))

    def main_loop(self, time_step: float = 0):
        running: bool = True

        while running:
            t_start: float = time.time()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.draw_all()
            while time.time() - t_start < time_step:
                pass

    def draw_all(self) -> None:
        self._DISPLAY.fill((0, 0, 0))
        pg.draw.circle(self._DISPLAY, (120, 30, 0), (0, 0), 50)
        self.draw_line_to_mouse()
        pg.display.flip()

    def draw_line_to_mouse(self) -> None:
        pg.draw.line(self._DISPLAY, (0, 210, 160), (0, 0), pg.mouse.get_pos())
