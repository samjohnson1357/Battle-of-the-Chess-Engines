"""
File Summary: Reads several different chess engines into Python.
"""

import chess.engine


def readXiphos():
    path = r"C:\Program Files\xiphos-master\bin\xiphos-0.6-w64-bmi2.exe"
    return chess.engine.SimpleEngine.popen_uci(path)

def readRybka():
    path = r"C:\Program Files\Rybka232a\Rybkav2.3.2a.mp.x64.exe"
    return chess.engine.SimpleEngine.popen_uci(path)

def readShredder():
    path = r"C:\Program Files (x86)\ShredderChess\Shredder Classic 5\EngineClassic5UCIx64.exe"
    return chess.engine.SimpleEngine.popen_uci(path)

def readKomodo():
    path = r'C:\Program Files\komodo-12.1.1_5a8fc2\Windows\komodo-12.1.1-64bit.exe'
    return chess.engine.SimpleEngine.popen_uci(path)

def readLeelaZero():
    path = r'C:\Program Files\lc0-v0.28.2-windows-cpu-dnnl\lc0.exe'
    return chess.engine.SimpleEngine.popen_uci(path)

def readStockfish():
    path = r'C:\Program Files\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe'
    return chess.engine.SimpleEngine.popen_uci(path)

def getOtherEngineDict():
    return {'Komodo':readKomodo(), 'Shredder':readShredder(), 'Stockfish':readStockfish(), 'Rybka':readRybka(), 'Xiphos':readXiphos()}

def getLeelaNameAndEngine():
    return 'Leela Zero', readLeelaZero()

