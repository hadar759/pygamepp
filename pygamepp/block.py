from typing import Tuple


class Block:
    def __init__(self, position: Tuple[int, int], occupied: bool):
        self.position = position
        self.occupied = occupied
