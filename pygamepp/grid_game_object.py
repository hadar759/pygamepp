from typing import List

import pygame


class GridGameObject:
    def __init__(self, sprite: pygame.sprite, position: List):
        self.sprite = sprite
        colorkey = self.sprite.get_at((0, 0))
        self.sprite.set_colorkey(colorkey)

        self.position = position

    def display_object(self, screen: pygame.Surface, block_size: int):
        screen.blit(self.sprite, (self.position[0] * block_size, self.position[1] * block_size))
