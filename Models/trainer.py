import sys

sys.path.append("..\EXO")
sys.setrecursionlimit(100000)

from Genetic import Agent, CrossOver, Mutation
from Tools import exo
import random as rnd

initialPath = "Models/Genetic/Gnomes/ID-4919.txt"

def RunGame(chromo1, chromo2):
    agent = [Agent(chromo1, 0), Agent(chromo2, 1)]

    board = exo.InitBoard()

    turn = 0
    n = 1
    while not exo.CheckGameEnd(board):
        move = agent[turn].FindBestMove(board)

        board[move // 3][move % 3] = str(turn)

        turn = abs(turn - 1)
        n += 1

    if exo.CheckWin(board, 0) == 1:
        return chromo1, 1
    elif exo.CheckWin(board, 1) == 1:
        return chromo2, 1
    else:
        return chromo1, 0
    
def Evolution(path):
    #get all chromosome in array
    with open(path, 'r') as f:
        chromosomes = [l.strip('\n\r ') for l in f.readlines()]

    #Get the winner in each match
    openChromos = []
    winCount = 0
    for i in range(0, len(chromosomes), 2):
        winnerChromo, winning = RunGame(chromosomes[i], chromosomes[(i + 1) % len(chromosomes)])

        openChromos.append(winnerChromo)

        winCount += winning

        # print(f'Winner is {winnerChromo.split(" ")[0]} {winnerChromo.split(" ")[1][:3]}...')
    print(winCount / (len(chromosomes) // 2))

    #randomly cross over them then mutate some of them
    rnd.shuffle(openChromos)
    for i in range(0, len(openChromos)):

        chromoMix = CrossOver(chromosomes[i], chromosomes[(i + rnd.randint(0, len(openChromos))) % len(chromosomes)])

        openChromos.append(chromoMix)

    openChromos = list(map(Mutation, openChromos))

    #register them as new gen
    path = path[:-4]

    try:
        path, gen = path.split('_Gen-')
        gen = int(gen)
    except:
        path = path
        gen = 0

    path = path + f'_Gen-{gen + 1}.txt'

    with open(path, 'w') as f:
        for chromo in openChromos:
            f.write(chromo + "\n")

    return path

if __name__ == "__main__":

    curPath = initialPath
    for i in range(1000):
        print(f'Gen {i} - Win rate ', end='')
        curPath = Evolution(curPath)
