import numpy as np
from board import Board
from stone import Stone


class Game:
    def start(self):
        board = Board()
        board.seleect_mode()
        while (board.count < 2
               and np.any(board.board == Stone.EMPTY)
               and np.any(board.board == Stone.BLACK)
               and np.any(board.board == Stone.WHITE)):
            board.print_board()
            board.input_stone()

        board.print_board()
        board.count_stones()
