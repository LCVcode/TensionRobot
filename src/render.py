import pygame as pg
import time


class RenderWindow:

    HEIGHT: int
    WIDTH: int
    _DISPLAY: pg.surface.Surface

    def __init__(self, width: int, height: int):
        self._DISPLAY = pg.display.set_mode((width, height))
