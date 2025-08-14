import numpy as np
import random
import copy
from stone import Stone


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

    def input_stone(self):
        print(f"現在のターン：{self.turn}")

        positions = self.check_all_puts()

        if self.mode == 1 and self.turn == self.computer:
            if self.difficulty == 1:
                if positions:
                    position = random.choice(positions)
                    print(f"コンピューターは{position}に置きました")
                    self.count = 0
                    self.put_stone(position)
                    return
                else:
                    print("コンピューターにおける場所がありませんでした。")
                    self.count += 1
                    self.turn = Stone.WHITE if self.turn == Stone.BLACK else Stone.BLACK
                    return
            else:
                if positions:
                    position = max(positions, key=self.calc_score)
                    print(f"コンピューターは{position}に置きました")
                    self.count = 0
                    self.put_stone(position)
                    return
                else:
                    print("コンピューターにおける場所がありませんでした。")
                    self.count += 1
                    self.turn = Stone.WHITE if self.turn == Stone.BLACK else Stone.BLACK
                    return

        if not positions:
            self.turn = Stone.WHITE if self.turn == Stone.BLACK else Stone.BLACK
            input("おける場所がありません。Enterを押してください")
            self.count += 1
            return

        for idx, pos in enumerate(positions):
            print(f"{idx} : {pos}", end=", ")
        self.count = 0

        while True:
            num = input("数字を選択してください: ")
            if num.isdigit() and 0 <= int(num) < len(positions):
                self.put_stone(positions[int(num)])
                break
            print("無効な入力です。もう一度入力してください。")
        print(f"{self.turn}を{positions[int(num)]}に置きました。")

    def check_all_puts(self):
        positions = []
        for i in range(8):
            for j in range(8):
                if self.check_put(i, j):
                    positions.append(f"{i}-{j}")
        return positions

    def put_stone(self, position):
        for dr, dc in self.directions:
            x, y = map(int, position.split('-'))
            if self.confirm_put(x, y, dr, dc):
                self.board[x, y] = self.turn
                while self.board[x + dr, y + dc] != self.turn:
                    x += dr
                    y += dc
                    self.board[x, y] = self.turn

        self.turn = Stone.WHITE if self.turn == Stone.BLACK else Stone.BLACK

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

    def calc_score(self, position):
        score = 0
        x, y = map(int, position.split('-'))
        empty_count = np.sum(self.board == Stone.EMPTY)

        # 序盤・中盤・終盤の評価パラメータ
        if empty_count > 40:
            corner_bonus = 200
            danger_penalty = -120
            center_bonus = 50
            edge_bonus = 20
            opponent_penalty_factor = 0.3
            return_count_factor = 0.5
        elif empty_count > 15:
            corner_bonus = 300
            danger_penalty = -200
            center_bonus = 30
            edge_bonus = 15
            opponent_penalty_factor = 0.5
            return_count_factor = 0.7
        else:
            corner_bonus = 1000
            danger_penalty = -50
            center_bonus = 0
            edge_bonus = 0
            opponent_penalty_factor = 0.7
            return_count_factor = 1.0

        # 角マス
        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        corner_adjacent = [[0, 1], [1, 0], [0, 6],
                           [1, 7], [6, 0], [7, 1], [6, 7], [7, 6]]

        if [x, y] in corners:
            score += corner_bonus
        elif [x, y] in corner_adjacent:
            score += danger_penalty
        elif 2 <= x <= 5 and 2 <= y <= 5:
            score += center_bonus  # 中央ボーナス
        elif (x == 0 or x == 7 or y == 0 or y == 7):
            score += edge_bonus    # 角以外の辺ボーナス

        # 挟める石の数
        score -= self.return_count(position) * return_count_factor

        # 次ターンの可能性
        score -= self.count_puts(position)

        # 相手の手を読む
        board_copy = copy.deepcopy(self)
        board_copy.put_stone(position)
        opponent_moves = board_copy.check_all_puts()
        if opponent_moves:
            worst_reply_score = max(board_copy.calc_score_basic(m)
                                    for m in opponent_moves)
            score -= worst_reply_score * opponent_penalty_factor

        # 終盤なら石差も加点
        if empty_count <= 15:
            black = np.sum(board_copy.board == Stone.BLACK)
            white = np.sum(board_copy.board == Stone.WHITE)
            if self.turn == Stone.BLACK:
                score += (black - white) * 5
            else:
                score += (white - black) * 5

        return score

    def calc_score_basic(self, position):
        score = 0
        x, y = map(int, position.split('-'))
        empty_count = np.sum(self.board == Stone.EMPTY)

        # 序盤・中盤・終盤の評価パラメータ
        if empty_count > 40:  # 序盤
            corner_bonus = 200
            danger_penalty = -120
            center_bonus = 50
            edge_bonus = 20
            return_count_factor = 0.5
        elif empty_count > 15:  # 中盤
            corner_bonus = 300
            danger_penalty = -200
            center_bonus = 30
            edge_bonus = 15
            return_count_factor = 0.7
        else:  # 終盤
            corner_bonus = 1000
            danger_penalty = -50
            center_bonus = 0
            edge_bonus = 0
            return_count_factor = 1.0

        # 角マス
        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        corner_adjacent = [[0, 1], [1, 0], [0, 6],
                           [1, 7], [6, 0], [7, 1], [6, 7], [7, 6]]

        if [x, y] in corners:
            score += corner_bonus
        elif [x, y] in corner_adjacent:
            score += danger_penalty
        elif 2 <= x <= 5 and 2 <= y <= 5:
            score += center_bonus
        elif (x == 0 or x == 7 or y == 0 or y == 7):
            score += edge_bonus

        # 挟める石の数
        score -= self.return_count(position) * return_count_factor

        # 次ターンの可能性
        score -= self.count_puts(position)

        # 終盤なら石差も加点
        if empty_count <= 15:
            board_copy = copy.deepcopy(self)
            board_copy.put_stone(position)
            black = np.sum(board_copy.board == Stone.BLACK)
            white = np.sum(board_copy.board == Stone.WHITE)
            if self.turn == Stone.BLACK:
                score += (black - white) * 5
            else:
                score += (white - black) * 5

        return score

    def count_puts(self, position):
        count = 0
        positions = self.predict_board(position)
        count = len(positions) * 20
        for position in positions:
            x, y = map(int, position.split('-'))
            if [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]:
                count += 600
            elif (x in [0, 7] and y in range(2, 6)) or (y in [0, 7] and x in range(2, 6)):
                count += 10
            next_positions = self.predict_board(position)
            count -= int(len(next_positions) / len(positions)) * 5

        return count

    def predict_board(self, position):
        board_copy = copy.deepcopy(self)
        board_copy.put_stone(position)
        return board_copy.check_all_puts()

    def return_count(self, position):
        count = 0
        board_copy = copy.deepcopy(self)
        for dr, dc in self.directions:
            x, y = map(int, position.split('-'))
            if board_copy.confirm_put(x, y, dr, dc):
                while board_copy.board[x + dr, y + dc] != self.turn:
                    x += dr
                    y += dc
                    if np.sum(self.board == Stone.EMPTY) >= 36:
                        count += 8
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        count -= 1
                    elif (x in range(2, 5) and y in range(2, 5)):
                        count += 1
        return count
