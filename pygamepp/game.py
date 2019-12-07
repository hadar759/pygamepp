from typing import List, Optional, Callable, Dict, Union

import pygame

from pygamepp.game_object import GameObject
from pygamepp.grid_game_object import GridGameObject

pygame.init()

EVENT_HANDLER_TYPE = Union[Callable[[pygame.event.EventType], None],
                           Callable[[], None]]


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
        self.event_handlers: Dict[int, EVENT_HANDLER_TYPE] = {}
        self.game_objects: List[GameObject, GridGameObject] = []
        self.last_pressed_key = 0

        self.background_image = pygame.image.load(background_path) if background_path else None

    def run(self):
        """Run the game"""
        clock = pygame.time.Clock()
        self.running = True
        self.set_event_handler(pygame.QUIT, self.quit)
        while self.running:
            self.start_of_loop()

            for event in pygame.event.get():
                if hasattr(event, "key"):
                    self.last_pressed_key = event.key

                event_function = self.event_handlers.get(event.type)
                if event_function:
                    try:
                        event_function(event)
                    except TypeError:
                        event_function()

            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))

            for game_object in self.game_objects:
                game_object.display_object(self.screen)

            self.end_of_loop()

            pygame.display.flip()

            clock.tick(self.refresh_rate)

    def set_event_handler(self, event_num: int, func: EVENT_HANDLER_TYPE):
        self.event_handlers[event_num] = func

    def create_timer(self, event_number: int, timer_time: int, repeat: bool = False):
        pygame.time.set_timer(event_number, timer_time, repeat)

    def start_of_loop(self):
        pass

    def end_of_loop(self):
        pass

    def quit(self):
        self.running = False
        pygame.quit()
