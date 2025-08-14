from src.stone import Stone
from board import Board
import random

from abc import abstractmethod, ABC


class Player(ABC):
    def __init__(self, name: str, color: Stone):
        self.name = name
        self.color = color

    @abstractmethod
    def move_stone(self, board: Board):
        pass


class HumanPlayer(Player):

    def move_stone(self, board: Board):
        positions = board.check_all_puts()

        if not positions:

            return None

        for idx, pos in enumerate(positions):
            print(f"{idx} : {pos}", end=", ")

        while True:
            num = input("数字を選択してください: ")
            if num.isdigit() and 0 <= int(num) < len(positions):
                return positions[int(num)]


class ComputerPlayer(Player):

    def move_stone(self, board: Board):
        positions = board.check_all_puts()
        if not positions:
            return None

        if board.difficulty == 1:
            return random.choice(positions)

        else:

            return max(positions, key=board.calc_score)
