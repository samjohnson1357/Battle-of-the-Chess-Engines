"""
File Summary: File processes evaluation data and then plots it very nicely.
"""

import matplotlib.pyplot as plt
import numpy as np
import math

def getLastSeenRealValue(arr):
    for val in arr[::-1]:
        if val is not None:
            return val

def replaceNoneValuesWithLastSeenRealValue(arr):
    """
    This is one approach. Instead of removing none values, it replaces them with their previously seen values.
    It modifies the array inplace.
    """
    lastSeenRealValue = getLastSeenRealValue(arr)
    arr[arr == None] = lastSeenRealValue

def removeNoneValuesFromArray(arr):
    """
    This is one approach. Unfortunately, it leads to one array having more values than the other.
    """
    return arr[arr != None]

def boundArrayMax(arr, val):
    """
    Function modifies the array in place.
    """
    arr[arr > val] = val

def boundArrayMin(arr, val):
    """
    Function modifies the array in place.
    """
    arr[arr < val] = val

def boundArrayMinAndMax(arr, val):
    boundArrayMin(arr, -val)
    boundArrayMax(arr, val)

def processEvaluationData(evalArr, value):
    """
    Evaluations may reach into the high positives or high negatives. One evaluation could also have more data
    than another, due to None values that represent a checkmate in the near future. This function places a bound
    on the evaluations and removes None values from the array.
    """
    evalArr = np.array(evalArr)
    # replaceNoneValuesWithLastSeenRealValue(evalArr)
    boundArrayMinAndMax(evalArr, value)
    return evalArr

def getMoveNumberData(evalArr):
    return range(1, len(evalArr) + 1)

def getLowerAndUpperYLimit(processedEvalData1, processedEvalData2):
    """
    Function returns the y-limit as a positive value.
    """
    aggregatedData = list(processedEvalData1)
    aggregatedData.extend(list(processedEvalData2))
    minVal = np.min(aggregatedData)
    maxVal = np.max(aggregatedData)
    limit = np.max([abs(minVal), abs(maxVal)])
    return math.ceil(limit+0.01)  # Ensure buffer value for 10.

def plotPovEvaluations(whiteName, blackName, result, terminationReason, whiteEvalHist, blackEvalHist, fileName):
    """
    This method uses the engine logo colors (green and red) to identify the engines.
    Each engine represents its current evaluation of the white player.
    """
    whiteLabel = '{} (White)'.format(whiteName)
    blackLabel = '{} (Black)'.format(blackName)
    title = 'Game Evaluation by Move ({} by {})'.format(result, terminationReason)

    boundary = 10
    whiteEvalHist = processEvaluationData(whiteEvalHist, boundary)
    blackEvalHist = processEvaluationData(blackEvalHist, boundary)

    plt.figure(figsize=(10, 5))

    ax = plt.axes()
    ax.set_facecolor('blue')

    # There are a couple of ways to set the y-limit. A fixed limit is far more consistent though between figures.
    # yLimit = getLowerAndUpperYLimit(whiteEvalHist, blackEvalHist)
    yLimit = 11
    ax.set_ylim(-yLimit, yLimit)

    plt.plot(getMoveNumberData(whiteEvalHist), whiteEvalHist, label=whiteLabel, color='white', marker='o')
    plt.plot(getMoveNumberData(blackEvalHist), blackEvalHist, label=blackLabel, color='black', marker='o')
    plt.axhline(y=0, color='red', linestyle='--', linewidth=1)
    plt.legend()
    plt.grid()

    plt.xlabel('Move Number')
    plt.ylabel('Evaluation in Pawns')
    plt.title(title)
    plt.savefig(fileName, dpi=400)  # Note: The default DPI is very low at 100.
    # plt.savefig(fileName)
    # plt.show()

