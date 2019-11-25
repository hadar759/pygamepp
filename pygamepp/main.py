# Hadar Dagan
# Cyber project - Crazy Planes
# Version 1.0
# November 17th, 2019

import ctypes

from pygamepp import game

USER32 = ctypes.windll.user32


def main():
    """Call the game and run it"""
    width = USER32.GetSystemMetrics(0)
    height = USER32.GetSystemMetrics(1)
    crazy_plane_game = game.Game(width, height, 75)
    crazy_plane_game.run()


if __name__ == "__main__":
    main()
