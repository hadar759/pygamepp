from typing import List

import pygame


class GridGameObject:
    def __init__(self, sprite: pygame.sprite, position: List, block_size):
        self.sprite = sprite
        colorkey = self.sprite.get_at((0, 0))
        self.sprite.set_colorkey(colorkey)

        self.position = position
        self.block_size = block_size

    def display_object(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.position[0] * self.block_size, self.position[1] * self.block_size))
