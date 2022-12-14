"""
File Summary: Uses an opening book to initialize the chess board to random-weighted positions several moves in.
"""

import chess.pgn
import chess
import chess.polyglot


class PolyglotOpeningBook:
    """
    A class is used so that the opening book only has to be loaded once and can be used multiple times.
    """
    def __init__(self):
        filePath = r'poly17\books\Perfect2017-LC0.bin'
        self.openingBook = chess.polyglot.open_reader(filePath)

    def generateStartingFen(self, nMoves):
        """
        Note: The number of moves is the number of moves for each player.
        """
        board = chess.Board()
        for i in range(nMoves*2):
            move = self.openingBook.weighted_choice(board).move
            board.push(move)
        return board.fen()

    def closeOpeningBook(self):
        self.openingBook.close()

    def generateMultipleStartingFens(self, nFens, nMoves):
        fenList = [self.generateStartingFen(nMoves) for _ in range(nFens)]
        self.closeOpeningBook()
        return fenList


if __name__ == '__main__':
    pass

