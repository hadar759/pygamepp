from typing import List

from pygamepp.block import Block


class Grid:
    def __init__(self, height: int, width: int, block_size: int):
        self.height = height
        self.width = width

        self.blocks = []
        for i in range(self.height):
            self.blocks.append([Block(j * block_size, i * block_size, False)
                                for j in range(self.width)])

    def is_a_legal_move(self, position: List[int]) -> bool:
        """Returns whether an object already occupies a given position"""
        return (0 <= position[0] < self.height
                and 0 <= position[1] < self.width
                and not self.blocks[position[0]][position[1]].occupied)

    def occupy_block(self, block_num):
        cur_block = self.blocks[block_num[0]][block_num[1]]
        cur_block.occupied = True

    def get_available_positions_around(self, position) -> List[List[int]]:
        """Return a list of all available positions around a given position"""
        available_spaces: List[List[int]] = []
        for i in range(2):
            for j in range(2):
                temp_positions = [
                    [position[0] + i, position[1] + j],
                    [position[0] + i, position[1] - j],
                    [position[0] - i, position[1] + j],
                    [position[0] - i, position[1] - j]
                ]
                for pos in temp_positions:
                    if self.is_a_legal_move(pos) and pos not in available_spaces:
                        available_spaces.append(pos)
        if len(available_spaces) == 0:
            available_spaces.append(position)
        return available_spaces
