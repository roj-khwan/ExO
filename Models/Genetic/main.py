import math
import random as rnd
from . import workshop as ws

class Agent:
    def __init__(self, chromosomeTxt : str, side : int) -> None:
        chromosomeTxt = chromosomeTxt.split(' ')

        self.chromosome = list(map(ws.DecryptGene, chromosomeTxt))
        self.side = side

    def FindBestMove(self, board):

        bestMove = -1
        bestValue = -math.inf
        for i in range(9):

            if board[i // 3][i % 3] != '_': continue

            x = self.CalcValue(board, f'0{i}')
            
            if x > bestValue:
                bestMove = i
                bestValue = x

        return bestMove
    
    def CalcValue(self, board, sinkID):
        genes = [gene for gene in self.chromosome if sinkID == f'{gene[2]}{gene[3]}']

        sumary = 0
        n = 0

        for gene in genes:

            weight = (gene[4] * 2 - 1) * (gene[5] / pow(9, ws.weightDigit))

            if gene[0] == 0:
                #sum += input * sign of weight * weight size
                inputVal = 0
                try:
                    if board[gene[1] // 3][gene[1] % 3] == str(self.side):
                        inputVal += 1
                    elif board[gene[1] // 3][gene[1] % 3] == str(abs(self.side - 1)):
                        inputVal -= 1
                except:
                    print(gene, self.chromosome[0])
                    exit()

                sumary += inputVal * weight
            else:
                #sum += processNode sum * sign * weight size
                nodeVal = self.CalcValue(board, f'{gene[0]}{gene[1]}')

                sumary += nodeVal * weight

            n += 1

        return 0 if n == 0 else sumary / n
    
def CrossOver(chromo1, chromo2):

    chromo1, chromo2 = (chromo1.split(' '), chromo2.split(' '))

    pivot = rnd.randint(0, len(chromo1))

    return ' '.join(chromo1[:pivot] + chromo2[pivot:])

def Mutation(chromoTxt):
    chromo = chromoTxt.split(' ')

    chromoTxt = ''

    for rawGene in chromo:

        gene = ws.DecryptGene(rawGene)

        r = rnd.random()
        while r <= ws.mutationRate:
            gene = ws.DecryptGene(rawGene)

            NewJean = ws.RandomGeneParams()

            index = rnd.randint(0, 3)

            if index <= 1:
                gene[0 + index * 2] = NewJean[0 + index * 2]
                gene[1 + index * 2] = NewJean[1 + index * 2]
            else:
                gene[2 + index] = NewJean[2 + index]

            if (not ws.CheckGeneParam(gene)):
                break

        gene = ws.EncryptGene(gene)

        chromoTxt += f'{gene} '

    return chromoTxt.strip(' ')