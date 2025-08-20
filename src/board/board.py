import numpy as np
from src.board.stone import Stone


class Board:
    difficulty = 0
    computer = Stone.WHITE
    mode = 0
    count = 0
    turn = Stone.BLACK
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]

    def __init__(self):
        self.board = np.full((8, 8), Stone.EMPTY)
        self.board[3, 3] = Stone.WHITE
        self.board[3, 4] = Stone.BLACK
        self.board[4, 3] = Stone.BLACK
        self.board[4, 4] = Stone.WHITE

    def seleect_mode(self):
        print("モードを選択してね\n1: 一人プレイ　2: 二人プレイ")
        while True:
            try:
                self.mode = int(input())
                if self.mode in [1, 2]:
                    break
                else:
                    print("1または2を入力してください")
            except ValueError:
                print("無効な入力です。1または2を入力してください")

        if self.mode == 1:
            print("難易度を選んでね\n 1: 簡単　2: 普通")
            while True:
                try:
                    self.difficulty = int(input())
                    if self.difficulty in [1, 2]:
                        break
                    else:
                        print("1または2を入力してください")
                except ValueError:
                    print("無効な入力です。1または2を入力してください")
            print(f"先手か後手を選んでね\n1: 先手{Stone.BLACK}　2: 後手{Stone.WHITE}")
            while True:
                try:
                    cointoss = int(input())
                    if cointoss in [1, 2]:
                        if cointoss == 2:
                            self.computer = Stone.BLACK
                        break
                    else:
                        print("1または2を入力してください")
                except ValueError:
                    print("無効な入力です。1または2を入力してください")

    def print_board(self):
        print("   " + "".join(f"{i:^4}" for i in range(8)))
        print("  +" + "---+" * 8)
        for i, row in enumerate(self.board):
            print(f"{i} |", end="")
            for stone in row:
                print(f" {stone} |", end="")
            print()
            print("  +" + "---+" * 8)

    def check_put(self, x, y):
        if self.board[x, y] != Stone.EMPTY:
            return False
        for dr, dc in self.directions:
            if self.confirm_put(x, y, dr, dc):
                return True
        return False

    def confirm_put(self, x, y, dr, dc):
        opponent = Stone.BLACK if self.turn == Stone.WHITE else Stone.WHITE
        r, c = x + dr, y + dc
        if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.turn:
                return True
        return False

    def check_all_puts(self):
        positions = []
        for i in range(8):
            for j in range(8):
                if self.check_put(i, j):
                    positions.append(f"{i}-{j}")
        return positions

    def put_stone(self, position):
        if position is None:
            self.count += 1
        else:
            for dr, dc in self.directions:
                x0, y0 = map(int, position.split('-'))
                if self.confirm_put(x0, y0, dr, dc):
                    x = x0
                    y = y0
                    self.board[x, y] = self.turn
                    while self.board[x + dr, y + dc] != self.turn:
                        x += dr
                        y += dc
                        self.board[x, y] = self.turn
        self.turn = self.turn.opponent()

    def count_stones(self):
        black = np.sum(self.board == Stone.BLACK)
        white = np.sum(self.board == Stone.WHITE)
        print(f"{Stone.BLACK} : {black}個, {Stone.WHITE} : {white}個")
        win = Stone.BLACK if black > white else Stone.WHITE if white > black else None
        if self.mode == 1:
            if win == self.computer:
                print("コンピュータの勝ちです！")
            elif win:
                print("プレイヤーの勝ちです！")
            else:
                print("引き分けです！")
            return
        if win:
            print(f"勝者は{win}です！")
        else:
            print("引き分けです！")

    def is_game_over(self):
        if self.count >= 2:
            return True
        if not np.any(self.board == Stone.EMPTY):
            return True
        if not np.any(self.board == Stone.BLACK) or not np.any(self.board == Stone.WHITE):
            return True
        return False
