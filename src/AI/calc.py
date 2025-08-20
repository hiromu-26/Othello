import copy
import numpy as np
from src.board.board import Board
from src.board.stone import Stone


class Calc:
    @staticmethod
    def calc_score(position, board: Board, stone: Stone = None):
        """
        1手打った場合の評価値を返す
        stone: 評価する側の石
        """
        if stone is None:
            stone = board.turn  # デフォルトは現在のターン

        x, y = map(int, position.split('-'))

        board_copy = copy.deepcopy(board)
        flipped_count = Calc.simulate_put(position, board_copy)
        if flipped_count == 0:
            return -9999  # 非合法手

        empty_count = np.sum(board.board == Stone.EMPTY)
        eval_params = Calc.get_eval_params(empty_count)

        score = 0

        # 座標スコア（角・辺・中央・危険なX-squares）
        score += Calc.position_score(x, y, eval_params)

        # 裏返し枚数
        score += flipped_count * eval_params['flip_factor']

        # モビリティ：自分の手の数
        my_moves = board_copy.check_all_puts()
        score += len(my_moves) * eval_params['mobility_factor']

        # 相手のモビリティ
        board_copy.turn = Stone.BLACK if stone == Stone.WHITE else Stone.WHITE
        opponent_moves = board_copy.check_all_puts()
        score -= len(opponent_moves) * eval_params['opponent_penalty_factor']

        # 安定石
        score += Calc.count_stable_stones(board_copy,
                                          stone) * eval_params['stable_stone_bonus']

        # 終盤の石差
        if empty_count <= 20:
            black = np.sum(board_copy.board == Stone.BLACK)
            white = np.sum(board_copy.board == Stone.WHITE)
            diff = black - white if stone == Stone.BLACK else white - black
            score += diff * eval_params['endgame_weight']

        return score

    @staticmethod
    def simulate_put(position, board: Board):
        """指定位置に石を置いて裏返し数を返す（不正手なら0）"""
        before_black = np.sum(board.board == Stone.BLACK)
        before_white = np.sum(board.board == Stone.WHITE)
        board.put_stone(position)
        after_black = np.sum(board.board == Stone.BLACK)
        after_white = np.sum(board.board == Stone.WHITE)
        return abs((after_black - before_black) + (after_white - before_white))

    @staticmethod
    def position_score(x, y, eval_params):
        """座標ごとの基本スコア"""
        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        corner_adjacent = [[0, 1], [1, 0], [0, 6], [1, 7],
                           [6, 0], [7, 1], [6, 7], [7, 6]]
        x_squares = [[1, 1], [1, 6], [6, 1], [6, 6]]  # 危険な角斜め

        if [x, y] in corners:
            return eval_params['corner_bonus']
        elif [x, y] in corner_adjacent:
            return eval_params['danger_penalty']
        elif [x, y] in x_squares:
            return eval_params['x_square_penalty']
        elif 2 <= x <= 5 and 2 <= y <= 5:
            return eval_params['center_bonus']
        elif x in [0, 7] or y in [0, 7]:
            return eval_params['edge_bonus']
        return 0

    @staticmethod
    def count_stable_stones(board: Board, stone: Stone):
        """角・辺に連結した安定石を数える"""
        stable = 0
        for i in range(8):
            for j in range(8):
                if board.board[i, j] == stone:
                    if i in [0, 7] or j in [0, 7]:
                        stable += 1
                    # 角周辺の安定石も加点
                    if (i in [1, 6] and j in [1, 6]) or (i in [0, 7] and j in [1, 6]) or (i in [1, 6] and j in [0, 7]):
                        stable += 1
        return stable

    @staticmethod
    def get_eval_params(empty_count):
        """序盤・中盤・終盤で重みを変える"""
        if empty_count > 40:  # 序盤
            return {
                'corner_bonus': 2000,
                'danger_penalty': -900,
                'x_square_penalty': -900,
                'center_bonus': 250,
                'edge_bonus': 50,
                'flip_factor': -0.2,
                'opponent_penalty_factor': 0.5,
                'endgame_weight': 0,
                'stable_stone_bonus': 4,
                'mobility_factor': 4
            }
        elif empty_count > 15:  # 中盤
            return {
                'corner_bonus': 2000,
                'danger_penalty': -400,
                'x_square_penalty': -500,
                'center_bonus': 50,
                'edge_bonus': 70,
                'flip_factor': 0,
                'opponent_penalty_factor': 0.7,
                'endgame_weight': 1,
                'stable_stone_bonus': 5,
                'mobility_factor': 5
            }
        else:  # 終盤
            return {
                'corner_bonus': 2000,
                'danger_penalty': -200,
                'x_square_penalty': -300,
                'center_bonus': 0,
                'edge_bonus': 100,
                'flip_factor': 0.3,
                'opponent_penalty_factor': 0.5,
                'endgame_weight': 8,
                'stable_stone_bonus': 10,
                'mobility_factor': 2
            }
