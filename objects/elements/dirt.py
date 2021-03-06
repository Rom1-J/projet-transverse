import random

from objects.constants import *


class Dirt(pg.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 4):
            self.tiles.append(
                pg.transform.scale(
                    pg.image.load(f"{TILES_PATH}/dirt{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return random.choice(self.tiles)
