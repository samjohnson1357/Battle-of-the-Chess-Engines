"""
File Summary: One utility function that is used in a couple of other modules.
"""

def parseStringOutcomeToNumber(outcome):
    """
    Returns the outcome as (1, 0), (0, 1), or (0.5, 0.5) in numerical form where the first value is for white.
    """
    vals = outcome.split('-')
    return eval(vals[0]), eval(vals[1])

