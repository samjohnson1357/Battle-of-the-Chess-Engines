"""
File Summary: Play a game of chess between two engines. Track their evaluations for each move.
"""

import itertools
import datetime as dt
import chess.engine
import chess.pgn
import process_eval_data
import utilities


def getScoreFromEvaluation(evaluation, pov):
    """
    Note: Function returns none if it is taking in a "mate evaluation".
    Otherwise, it returns the white score divided by 100.
    """
    povScoreObj = evaluation['score']

    if pov == 'white':
        scoreObj = povScoreObj.white()
    elif pov == 'black':
        scoreObj = povScoreObj.black()
    elif pov == 'relative':
        scoreObj = povScoreObj.relative
    else:
        raise Exception('The pov parameter must be "white", "black", or "relative"')

    return scoreObj.score(mate_score=2000) / 100

def getMoveFromEvaluation(evaluation):
    return evaluation['pv'][0]

class ChessGame:
    def __init__(self, whiteEngine, blackEngine, whiteEngineName, blackEngineName, startingFen, secondsPerMove):
        self.__whiteEngine = whiteEngine
        self.__blackEngine = blackEngine
        self.__whiteEngineName = whiteEngineName
        self.__blackEngineName = blackEngineName

        # Initialize the board.
        if startingFen is not None:
            self.__board = chess.Board(fen=startingFen)
        else:
            self.__board = chess.Board()

        # Initialize other important variables.
        self.__searchTerminationObj = chess.engine.Limit(time=secondsPerMove)
        self.__whiteEvalHistory = []  # Instance variables have to be used here for player color identification.
        self.__blackEvalHistory = []
        self.engineCycleObj = self.__getEngineCycleObject()

    def __engineSelectsMove(self, engine):
        evaluation = engine.analyse(self.__board, self.__searchTerminationObj)
        move = getMoveFromEvaluation(evaluation)
        score = getScoreFromEvaluation(evaluation, 'relative')  # You can change the evaluation POV here.
        return move, score

    def __getEngineCycleObject(self):
        """
        The cycle object enables us to switch between engines every move of the game.
        """
        cycle = [
            [self.__whiteEngine, self.__whiteEvalHistory],
            [self.__blackEngine, self.__blackEvalHistory]
        ]
        return itertools.cycle(cycle)

    def __getStringOutcome(self):
        return self.__board.outcome(claim_draw=True).result()

    def __getNumericalOutcome(self):
        """
        Returns the outcome as (1, 0), (0, 1), or (0.5, 0.5) in numerical form where the first value is for white.
        """
        outcome = self.__getStringOutcome()
        return utilities.parseStringOutcomeToNumber(outcome)

    def __getOutcomeReason(self):
        return self.__board.outcome(claim_draw=True).termination.name.title()

    def __getPgnObj(self):
        """
        Note: If a custom starting position is used, python-chess automatically sets the FEN header.
        """
        pgn = chess.pgn.Game.from_board(self.__board)
        pgn.headers['Event'] = 'Regular game'
        pgn.headers['Site'] = 'Dell Laptop'
        pgn.headers['Date'] = str(dt.date.today())
        pgn.headers['Round'] = '1'
        pgn.headers['White'] = self.__whiteEngineName
        pgn.headers['Black'] = self.__blackEngineName
        pgn.headers['Result'] = self.__getStringOutcome()
        pgn.headers['Termination'] = self.__getOutcomeReason()
        pgn.headers['TimeControl'] = str(self.__searchTerminationObj.time)
        pgn.headers['Time'] = str(dt.datetime.now().time())
        pgn.headers['WhiteEvalHistory'] = str(self.__whiteEvalHistory)
        pgn.headers['BlackEvalHistory'] = str(self.__blackEvalHistory)
        return pgn

    def __getFilePath(self, pgn):
        """
        Returns either the pgn file path or the jpg file path. They are the same except for the extension.
        """
        dtString = str(dt.datetime.now()).replace(':', ';')
        if pgn:
            return 'pgn-files/{} (White) vs {} (Black) @ {}.pgn'.format(self.__whiteEngineName, self.__blackEngineName, dtString)
        else:
            return 'pgn-files/{} (White) vs {} (Black) @ {}.jpg'.format(self.__whiteEngineName, self.__blackEngineName, dtString)

    def __savePgnToFile(self):
        pgn = self.__getPgnObj()
        fileName = self.__getFilePath(True)
        file = open(fileName, 'wt')
        file.write(str(pgn))
        file.close()

    def __saveEvaluationPlot(self):
        """
        This method uses the engine logo colors (green and red) to identify the engines.
        Each engine represents its current evaluation of the white player.
        """
        process_eval_data.plotPovEvaluations(self.__whiteEngineName, self.__blackEngineName, self.__getStringOutcome(),
                                             self.__getOutcomeReason(), self.__whiteEvalHistory, self.__blackEvalHistory,
                                             self.__getFilePath(False))

    def playGame(self):
        # Keep making moves until the game ends.
        while not self.__board.is_game_over(claim_draw=True):
            engine, evalList = next(self.engineCycleObj)
            move, score = self.__engineSelectsMove(engine)
            self.__board.push(move)
            evalList.append(score)

            print('Move:', move)
            print('Board:')
            print(self.__board)

        self.__savePgnToFile()
        self.__saveEvaluationPlot()
        return self.__getNumericalOutcome(), self.__getOutcomeReason()


if __name__ == '__main__':
    import read_engines
    leelaName, leelaEngine = read_engines.getLeelaNameAndEngine()
    otherEngineDict = read_engines.getOtherEngineDict()
    otherEngineName = 'Xiphos'
    game = ChessGame(otherEngineDict[otherEngineName], leelaEngine, otherEngineName, leelaName, None, 10)
    game.playGame()


