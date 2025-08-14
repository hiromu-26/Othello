
from src.board import Board
from src.stone import Stone
from src.player import HumanPlayer, ComputerPlayer, Player


class Game:

    def start(self):
        board = Board()
        board.seleect_mode()
        player1 = HumanPlayer("Player1", board.computer.opponent())
        if board.mode == 1:
            player2 = ComputerPlayer("Computer", board.computer)
        else:
            player2 = HumanPlayer("Player2", board.computer)
        players = {Stone.BLACK: player1, Stone.WHITE: player2} if board.computer.is_white() else {
            Stone.BLACK: player2, Stone.WHITE: player1}

        while (not board.is_game_over()):
            self.play_turn(players, board)

        board.print_board()
        board.count_stones()

    def play_turn(self, players, board: Board):
        player = players[board.turn]
        board.print_board()
        print(f"現在のターン：{board.turn}")
        position = player.move_stone(board)
        board.put_stone(position)
