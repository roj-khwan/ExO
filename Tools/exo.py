def InitBoard(): return [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]

def PrintBoard(board):
    dicts = {
        '0' : 'O',
        '1' : 'X',
        '_' : '_'
    }

    for i in board:
        print(''.join([dicts[j] for  j in i]))

def CheckWin(board, side):

    #verti n hori
    for i in range(3):

        #verti
        if all([board[i][j] == str(side) for j in range(3)]):
            return 1
        elif all([board[i][j] == str(abs(side - 1)) for j in range(3)]):
            return -1
        
        #hori
        if all([board[j][i] == str(side) for j in range(3)]):
            return 1
        elif all([board[j][i] == str(abs(side - 1)) for j in range(3)]):
            return -1

    #right slash
    if all([board[i][i] == str(side) for i in range(3)]):
        return 1
    elif all([board[i][i] == str(abs(side - 1)) for i in range(3)]):
        return -1
    
    #left slash
    if all([board[2 - i][i] == str(side) for i in range(3)]):
        return 1
    elif all([board[2 - i][i] == str(abs(side - 1)) for i in range(3)]):
        return -1
    
    return 0

def CheckEmptyByPos(board, move): return board[move // 3][move % 3] == '_'

def CheckEmptyByXY(board, x, y): return board[y][x] == '_'

def CheckGameEnd(board) -> bool: return CheckWin(board, 0) != 0 or all([not CheckEmptyByPos(board, i) for i in range(9)])