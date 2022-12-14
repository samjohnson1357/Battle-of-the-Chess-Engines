"""
File Summary: Read a PGN file into Python. You can also read the all important evaluation data from these files.
"""

import chess.pgn
import ast
import os
import pandas as pd
from collections import Counter

import process_eval_data
import utilities
from read_engines import *


class PgnFileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        file = open(filePath, 'rt')
        self.pgn = chess.pgn.read_game(file)

    def getWhiteEvalHistory(self):
        return ast.literal_eval(self.pgn.headers['WhiteEvalHistory'])

    def getBlackEvalHistory(self):
        return ast.literal_eval(self.pgn.headers['BlackEvalHistory'])

    def getWhiteName(self):
        return self.pgn.headers['White']

    def getBlackName(self):
        return self.pgn.headers['Black']

    def getResultAsString(self):
        return self.pgn.headers['Result']

    def getResultAsNumber(self):
        resultStr = self.getResultAsString()
        return utilities.parseStringOutcomeToNumber(resultStr)

    def getTermination(self):
        return self.pgn.headers['Termination']

    def __getImageFilePath(self):
        return self.filePath.replace('.pgn', '.jpg')

    def plotEvaluationsFromPgn(self):
        imagePath = self.__getImageFilePath()
        process_eval_data.plotPovEvaluations(self.getWhiteName(), self.getBlackName(), self.getResultAsString(),
                                             self.getTermination(), self.getWhiteEvalHistory(), self.getBlackEvalHistory(), imagePath)


def getPgnFileList():
    directory = 'pgn-files'
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('pgn')]

def getSummaryDfSkeleton():
    df = pd.DataFrame(data=0, index=['Komodo', 'Shredder', 'Stockfish', 'Rybka', 'Xiphos'],
                      columns=['Leela White Points', 'Leela White Missed Points', 'Leela Black Points', 'Leela Black Missed Points'])
    df.index.name = 'Other Engine'
    return df

def readAllPgnFilesIntoDf(saveFile):
    summaryDf = getSummaryDfSkeleton()
    fileList = getPgnFileList()
    for file in fileList:
        pgnFileReader = PgnFileReader(file)

        whiteName = pgnFileReader.getWhiteName()
        blackName = pgnFileReader.getBlackName()
        outcome = pgnFileReader.getResultAsNumber()

        if whiteName == 'Leela Zero':
            # If Leela is white, it gets the first value of the outcome.
            summaryDf.loc[blackName, 'Leela White Points'] += outcome[0]
            summaryDf.loc[blackName, 'Leela White Missed Points'] += outcome[1]
        elif blackName == 'Leela Zero':
            # If Leela is black, it gets the second value of the outcome.
            summaryDf.loc[whiteName, 'Leela Black Points'] += outcome[1]
            summaryDf.loc[whiteName, 'Leela Black Missed Points'] += outcome[0]
        else:
            raise Exception('Neither player is Leela Zero')

    if saveFile:
        summaryDf.to_csv('All Game Summary.csv')
    return summaryDf

def readSavedCsvFile():
    return pd.read_csv('All Game Summary.csv', index_col='Other Engine')

def saveEvaluationPlotsForAllPgnFiles():
    for file in getPgnFileList():
        print(file)
        pgnFileReader = PgnFileReader(file)
        pgnFileReader.plotEvaluationsFromPgn()

def getEngineWithFewestNumberOfGames():
    """
    After stopping the code from running, one engine will inevitably have more games done than another.
    This function automatically calculates the number of games each engine has played.
    That way, we can play more games with those that haven't played very many.
    """
    engineList = []
    for file in getPgnFileList():
        fileReader = PgnFileReader(file)
        engineList.append(fileReader.getWhiteName())
        engineList.append(fileReader.getBlackName())
    counter = Counter(engineList)
    return counter.most_common()[-1][0]


if __name__ == '__main__':
    print(getEngineWithFewestNumberOfGames())
    # saveEvaluationPlotsForAllPgnFiles()

