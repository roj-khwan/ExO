import sys
import math

sys.path.append("..\EXO")

import Tools.exo as exo

fitness = 3

def Minimax(board, isMax, depth, side, maxDepth):
    score = exo.CheckWin(board, side)

    if (exo.CheckGameEnd(board) or maxDepth <= depth): return score / (depth + 1)

    if isMax:
        bestScore = -100

        for i in range(9):

            if not exo.CheckEmpty(board, i): continue

            board[i // 3][i % 3] = f'{side}'

            score = Minimax(board, not isMax, depth + 1, side, maxDepth)

            bestScore = max(bestScore, score)

            board[i // 3][i % 3] = '_'

        return bestScore
    else:
        bestScore = 100

        for i in range(9):

            if not exo.CheckEmpty(board, i): continue

            board[i // 3][i % 3] = f'{abs(side - 1)}'

            score = Minimax(board, not isMax, depth + 1, side, maxDepth)

            bestScore = min(bestScore, score)

            board[i // 3][i % 3] = '_'

        return bestScore

 
def BestMove(board , side, maxDepth):
    bestMove = -1
    bestScore = -math.inf

    for i in range(9):

        if not exo.CheckEmpty(board, i): continue

        board[i // 3][i % 3] = f'{side}'

        score = Minimax(board, False, 0, side, maxDepth)
        # print(i, score)

        if score > bestScore:
            bestScore = score
            bestMove = i

        board[i // 3][i % 3] = '_'

    return bestMove

