import ctypes

from pygamepp import game


def main():
    """Call the game and run it"""
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    game = game.Game(width, height, 75)
    game.run()


if __name__ == "__main__":
    main()
