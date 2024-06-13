import sys
import math

sys.path.append("..\EXO")

from Genetic import Agent, CrossOver, Mutation, workshop as ws
from Minimax import BestMove
from Tools import exo
import random as rnd


def RunGameByChromosome(chromo1, chromo2):
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
        return chromo1
    elif exo.CheckWin(board, 1) == 1:
        return chromo2
    else:
        return chromo1

def SelectionAnarchy(chromos : list):
    
    rank = []
    openChromos = chromos.copy()

    n = 0
    while len(openChromos) > 1:
        chromo1, chromo2 = openChromos.pop(0), openChromos.pop(0)


        winnerChromo = RunGameByChromosome(chromo1, chromo2)
        loserChromo = chromo1 if chromo2 == winnerChromo else chromo2

        openChromos.append(winnerChromo)
        rank.append(loserChromo)
        n += 1

    rank.extend(openChromos)

    return rank[math.floor((1 - ws.selectionRate) * len(rank)):]

def SelectionByCoach(chromos : list):
    rank = []

    difficulty = 0
    nextRound = []
    openChromos = chromos.copy()
    while len(rank) != len(chromos):
        board = exo.InitBoard()

        chromosome = openChromos.pop(0)

        agent = Agent(chromosome, 0)

        turn = 0
        n = 1
        while not exo.CheckGameEnd(board):
            if turn == 0:
                move = agent.FindBestMove(board)
            else:
                move = BestMove(board, 1, difficulty)

            board[move // 3][move % 3] = str(turn)

            turn = abs(turn - 1)
            n += 1

        win = exo.CheckWin(board, 0)

        if difficulty > 3:
            if win == -1:
                rank.append(chromosome)
            elif win == 0 :
                rank.append(chromosome)
            else:
                nextRound.append(chromosome)
        else:
            if exo.CheckWin(board, 0) == -1:
                rank.append(chromosome)
            else:
                nextRound.append(chromosome)

        if len(openChromos) == 0:
            openChromos = nextRound.copy()
            nextRound = []
            difficulty += 1
            print(f'diff = {difficulty} left - {len(chromos) - len(rank)}')

    return rank[math.floor((1 - ws.selectionRate) * len(rank)):]


    
def Evolution(path):
    #get all chromosome in array
    with open(path, 'r') as f:
        chromosomes = [l.strip('\n\r ') for l in f.readlines()]

    #Get the winner in each match
    winningChromos = SelectionByCoach(chromosomes)

    #make them match number of chromosome
    openChromos = [winningChromos[i % len(winningChromos)] for i in range(len(chromosomes))]

    rnd.shuffle(openChromos)

    #set pivot and randomly cross over them
    pivot = math.ceil(ws.crossoverRate * len(openChromos))
    crossRange = list(range(pivot))

    rnd.shuffle(crossRange)
    for i in range(pivot):
        first, second = i, crossRange[i]

        chromoMix = CrossOver(chromosomes[first], chromosomes[second])

        openChromos[first] = chromoMix

    #mutaton some of them
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

    # initialPath = "Models/Genetic/Gnomes/ID-4919.txt"

    # curPath = initialPath
    # for i in range(100):
    #     print(f'Gen {i}')
    #     curPath = Evolution(curPath)

    testPath = "Models/Genetic/Gnomes/ID-4919_Gen-20.txt"

    #get all chromosome in array
    with open(testPath, 'r') as f:
        chromosomes = [l.strip('\n\r ') for l in f.readlines()]

    chroms = SelectionByCoach(chromosomes)

    for i in chroms[::-1]:
        print(chromosomes.index(i))

    # agent = Agent('0000011999', 0)

    # board = [
    #     ['0', '_', '_'],
    #     ['_', '_', '_'],
    #     ['_', '_', '_']
    # ]

    # print(agent.FindBestMove(board))