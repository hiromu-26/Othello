from enum import Enum


class Stone(Enum):
    EMPTY = ' '
    BLACK = '○'
    WHITE = '●'

    def __str__(self):
        return self.value

    def opponent(self) -> 'Stone':
        if self == Stone.BLACK:
            return Stone.WHITE
        elif self == Stone.WHITE:
            return Stone.BLACK
        else:
            raise ValueError("石が白か黒ではありません")

    def is_black(self) -> bool:
        return self == Stone.BLACK

    def is_white(self) -> bool:
        return self == Stone.WHITE

    def is_empty(self) -> bool:
        return self == Stone.EMPTY
