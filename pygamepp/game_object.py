import pygame


class GameObject:
    def __init__(self, sprite: pygame.sprite, position):
        self.sprite = sprite
        colorkey = self.sprite.get_at((0, 0))
        self.sprite.set_colorkey(colorkey)

        self.position = position

    def display_object(self, screen):
        screen.blit(self.sprite, self.position)
