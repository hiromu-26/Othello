from src.board import Board
import numpy as np
from src.stone import Stone
import copy


class Calc:
    @staticmethod
    def calc_score(position, board: Board):
        score = 0
        x, y = map(int, position.split('-'))
        empty_count = np.sum(board.board == Stone.EMPTY)
        eval_params = Calc.get_eval_params(empty_count)

        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        corner_adjacent = [[0, 1], [1, 0], [0, 6],
                           [1, 7], [6, 0], [7, 1], [6, 7], [7, 6]]

        if [x, y] in corners:
            score += eval_params['corner_bonus']
        elif [x, y] in corner_adjacent:
            score += eval_params['danger_penalty']
        elif 2 <= x <= 5 and 2 <= y <= 5:
            score += eval_params['center_bonus']
        elif (x == 0 or x == 7 or y == 0 or y == 7):
            score += eval_params['edge_bonus']

        score -= Calc.return_count(position, board) * \
            eval_params['return_count_factor']
        score -= Calc.count_puts(position, board)

        board_copy = copy.deepcopy(board)
        board_copy.put_stone(position)
        opponent_moves = board_copy.check_all_puts()
        if opponent_moves:
            worst_reply_score = max(Calc.calc_score_basic(m, board_copy)
                                    for m in opponent_moves)
            score -= worst_reply_score * eval_params['opponent_penalty_factor']

        if empty_count <= 15:
            black = np.sum(board_copy.board == Stone.BLACK)
            white = np.sum(board_copy.board == Stone.WHITE)
            if board.turn == Stone.BLACK:
                score += (black - white) * 5
            else:
                score += (white - black) * 5
        return score

    @staticmethod
    def get_eval_params(empty_count):
        if empty_count > 40:
            return {'corner_bonus': 200, 'danger_penalty': -120, 'center_bonus': 50, 'edge_bonus': 20,
                    'return_count_factor': 0.5, 'opponent_penalty_factor': 0.3}
        elif empty_count > 15:
            return {'corner_bonus': 300, 'danger_penalty': -200, 'center_bonus': 30, 'edge_bonus': 15,
                    'return_count_factor': 0.7, 'opponent_penalty_factor': 0.5}
        else:
            return {'corner_bonus': 1000, 'danger_penalty': -50, 'center_bonus': 0, 'edge_bonus': 0,
                    'return_count_factor': 1.0, 'opponent_penalty_factor': 0.7}

    @staticmethod
    def count_puts(position, board):
        positions = Calc.predict_board(position, board)
        count = len(positions) * 20
        next_positions_all = {pos: Calc.predict_board(
            pos, board) for pos in positions}
        for pos in positions:
            x, y = map(int, pos.split('-'))
            if [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]:
                count += 600
            elif (x in [0, 7] and y in range(2, 6)) or (y in [0, 7] and x in range(2, 6)):
                count += 10
            next_positions = next_positions_all[pos]
            count -= int(len(next_positions) / len(positions)) * 5
        return count

    @staticmethod
    def calc_score_basic(position, board):
        score = 0
        x, y = map(int, position.split('-'))
        empty_count = np.sum(board.board == Stone.EMPTY)
        eval_params = Calc.get_eval_params(empty_count)

        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        corner_adjacent = [[0, 1], [1, 0], [0, 6],
                           [1, 7], [6, 0], [7, 1], [6, 7], [7, 6]]

        if [x, y] in corners:
            score += eval_params['corner_bonus']
        elif [x, y] in corner_adjacent:
            score += eval_params['danger_penalty']
        elif 2 <= x <= 5 and 2 <= y <= 5:
            score += eval_params['center_bonus']
        elif (x == 0 or x == 7 or y == 0 or y == 7):
            score += eval_params['edge_bonus']

        score -= Calc.return_count(position, board) * \
            eval_params['return_count_factor']
        score -= Calc.count_puts(position, board)

        if empty_count <= 15:
            board_copy = copy.deepcopy(board)
            board_copy.put_stone(position)
            black = np.sum(board_copy.board == Stone.BLACK)
            white = np.sum(board_copy.board == Stone.WHITE)
            if board.turn == Stone.BLACK:
                score += (black - white) * 5
            else:
                score += (white - black) * 5
        return score

    @staticmethod
    def predict_board(position, board):
        board_copy = copy.deepcopy(board)
        board_copy.put_stone(position)
        return board_copy.check_all_puts()

    @staticmethod
    def return_count(position, board):
        count = 0
        board_copy = copy.deepcopy(board)
        for dr, dc in board.directions:
            x, y = map(int, position.split('-'))
            if board_copy.confirm_put(x, y, dr, dc):
                while board_copy.board[x + dr, y + dc] != board.turn:
                    x += dr
                    y += dc
                    if np.sum(board.board == Stone.EMPTY) >= 36:
                        count += 8
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        count -= 1
                    elif (x in range(2, 5) and y in range(2, 5)):
                        count += 1
        return count
