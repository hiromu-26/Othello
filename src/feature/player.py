from src.board.stone import Stone
from src.board.board import Board
from src.AI.othello_ai import OthelloAI
import random

from abc import abstractmethod, ABC


class Player(ABC):
    def __init__(self, name: str, color: Stone):
        self.name = name
        self.color = color

    def __str__(self):
        return self.name

    @abstractmethod
    def move_stone(self, board: Board):
        pass

    def display_stone(self, position=None):
        if position is None:
            print(f"{self}における場所がありませんでした。")

        else:
            print(f"{self}は{position}に置きました")


class HumanPlayer(Player):

    def move_stone(self, board: Board):
        positions = board.check_all_puts()

        if not positions:
            self.display_stone()
            return None

        for idx, pos in enumerate(positions):
            print(f"{idx} : {pos}", end=", ")

        while True:
            num = input("数字を選択してください: ")
            if num.isdigit() and 0 <= int(num) < len(positions):
                self.display_stone(positions[int(num)])

                return positions[int(num)]
            print("無効な入力です。もう一度入力してください。")


class ComputerPlayer(Player):

    def move_stone(self, board: Board):
        positions = board.check_all_puts()
        if not positions:
            self.display_stone()
            return None

        ai = OthelloAI()  # デフォルト探索深さで初期化

        if board.difficulty == 1:
            # 難易度1はランダム
            position = random.choice(positions)
        else:
            # 難易度2は MiniMax + α-β
            position = ai.choose_move(board)
            if position is None:
                # 万一AIが合法手を返さない場合
                position = random.choice(positions)

        self.display_stone(position)
        return position
