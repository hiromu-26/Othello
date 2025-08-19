import copy
from src.stone import Stone
from src.board import Board
from src.calc import Calc


class OthelloAI:
    def __init__(self, depth=5):
        self.depth = depth  # 探索の深さ

    def minimax(self, board: Board, depth, alpha, beta, maximizing_player: bool, stone: Stone):
        """MiniMax + α-β枝刈り"""
        if depth == 0 or board.is_game_over():
            score = self.evaluate_board(board, stone)
            return score, None

        legal_moves = board.check_all_puts()
        if not legal_moves:
            # パスしてターン交代
            board_copy = copy.deepcopy(board)
            board_copy.put_stone(None)
            score, _ = self.minimax(
                board_copy, depth-1, alpha, beta, not maximizing_player, stone)
            return score, None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board_copy = copy.deepcopy(board)
                board_copy.put_stone(move)
                eval_score, _ = self.minimax(
                    board_copy, depth-1, alpha, beta, False, stone)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board_copy = copy.deepcopy(board)
                board_copy.put_stone(move)
                eval_score, _ = self.minimax(
                    board_copy, depth-1, alpha, beta, True, stone)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board: Board, stone: Stone):
        """盤面全体の評価（AI目線）"""
        positions = board.check_all_puts()
        if not positions:
            # パスや終局のとき
            black = sum(row.count(Stone.BLACK) for row in board.board)
            white = sum(row.count(Stone.WHITE) for row in board.board)
            return black - white if stone == Stone.BLACK else white - black
        scores = [Calc.calc_score(pos, board, stone) for pos in positions]
        return max(scores)

    def choose_move(self, board: Board):
        """実際に使う手を返す。候補手スコアを出力"""
        stone = board.turn  # AIの石
        legal_moves = board.check_all_puts()
        move_scores = []

        for move in legal_moves:
            board_copy = copy.deepcopy(board)
            board_copy.put_stone(move)
            score, _ = self.minimax(
                board_copy, self.depth-1, float('-inf'), float('inf'), False, stone)
            move_scores.append((move, score))

        # スコア順に表示
        print("候補手とスコア:")
        for move, score in move_scores:
            print(f"{move} : {score}")

        # 最大スコアの手を選択
        best_move = max(move_scores, key=lambda x: x[1])[0]
        print(f"AIが選んだ手: {best_move}")
        return best_move
