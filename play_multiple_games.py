"""
File Summary: Leela Zero is pitted against each of the other engines at randomly initialized board positions.
"""

import opening_book
import read_engines
import play_single_game
import read_pgn_files


def playRoundBetweenEngines(engine1, engine2, engine1Name, engine2Name, startFen, secondsPerMove):
    """
    Function generates a starting position and each engines plays as white once and black once on the selected board.
    """

    # If there isn't a starting FEN, we generate one.
    if startFen is None:
        openingBook = opening_book.PolyglotOpeningBook()
        startFen = openingBook.generateStartingFen(5)

    # Engine one as white
    chessGame = play_single_game.ChessGame(engine1, engine2, engine1Name, engine2Name, startFen, secondsPerMove)
    outcome, reason = chessGame.playGame()
    print('White:', engine1Name, 'Black:', engine2Name)
    print(outcome, reason)

    # Engine one as black
    chessGame = play_single_game.ChessGame(engine2, engine1, engine2Name, engine1Name, startFen, secondsPerMove)
    outcome, reason = chessGame.playGame()
    print('White:', engine2Name, 'Black:', engine1Name)
    print(outcome, reason)

def playGamesContinuously(secondsPerMove):
    """
    This function just keeps playing chess games between Leela and another player until you stop it.
    The only issue here is that after multiple starts and stops it will result in an uneven number of games between players.
    """
    leelaName, leelaEngine = read_engines.getLeelaNameAndEngine()
    otherEngineDict = read_engines.getOtherEngineDict()
    while True:
        for otherEngineName in otherEngineDict.keys():
            playRoundBetweenEngines(leelaEngine, otherEngineDict[otherEngineName], leelaName, otherEngineName, None, secondsPerMove=secondsPerMove)

def playOnEngineWithTheFewestGames():
    """
    This approach is valuable because it ensures that each of the engines gets to play the same number of games.
    """
    otherEngineName = read_pgn_files.getEngineWithFewestNumberOfGames()
    print('Chosen Engine:', otherEngineName)
    leelaName, leelaEngine = read_engines.getLeelaNameAndEngine()
    otherEngineDict = read_engines.getOtherEngineDict()
    playRoundBetweenEngines(leelaEngine, otherEngineDict[otherEngineName], leelaName, otherEngineName, None, secondsPerMove=10)


if __name__ == '__main__':
    # while True:
    #     playOnEngineWithTheFewestGames()
    playGamesContinuously(secondsPerMove=0.1)

