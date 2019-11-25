# Hadar Dagan
# Cyber project - Crazy Planes
# Version 1.0
# November 17th, 2019

from typing import List, Optional, Callable, Dict

import pygame

from pygamepp.game_object import GameObject
from pygamepp.grid_game_object import GridGameObject

pygame.init()


class Game:
    def __init__(self,
                 width: int,
                 height: int,
                 refresh_rate: int = 60,
                 background_path: Optional[str] = None):

        self.width, self.height = width, height
        self.refresh_rate = refresh_rate
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Create our game grid
        # self.grid_size = self.get_grid_size_input()
        # self.grid = Grid(self.grid_size

        self.running = False
        self.event_handlers: Dict[int, Callable[[pygame.event.EventType], None]] = {}
        self.game_objects: List[GameObject, GridGameObject] = []

        self.background_image = pygame.image.load(background_path) if background_path else None

    def run(self):
        """Run the game"""
        clock = pygame.time.Clock()
        self.set_event_handler(pygame.QUIT, self.quit)
        self.set_event_handler(pygame.KEYDOWN, self.keyboard_actions)
        for event in pygame.event.get():
            event_function = self.event_handlers.get(event.type)

            if event_function:
                if event_function == self.keyboard_actions:
                    event_function(event)
                else:
                    event_function()

        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

        for game_object in self.game_objects:
            game_object.display_object(self.screen)

        pygame.display.flip()

        clock.tick(self.refresh_rate)

    def set_event_handler(self, event_num: int, func: Callable[[pygame.event.EventType], None]):
        self.event_handlers[event_num] = func

    def create_timer(self, event_number: int, timer_time: int):
        pygame.time.set_timer(event_number, timer_time)

    def keyboard_actions(self, event):
        self.event_handlers[event.key]()

    def quit(self):
        self.running = False
        pygame.quit()

