import math
from . import workshop

class Agent:
    def __init__(self, chromosomeTxt : str, side : int) -> None:
        chromosomeTxt = chromosomeTxt.split(' ')

        self.chromosome = list(map(workshop.DecryptGene, chromosomeTxt))
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

            weight = (gene[4] * 2 - 1) * (gene[5] / pow(9, workshop.weightDigit))

            if gene[0] == 0:
                #sum += input * sign of weight * weight size
                inputVal = 0
                if board[gene[1] // 3][gene[1] % 3] == str(self.side):
                    inputVal += 1
                elif board[gene[1] // 3][gene[1] % 3] == str(abs(self.side - 1)):
                    inputVal -= 1

                sumary += inputVal * weight
            else:
                #sum += processNode sum * sign * weight size
                nodeVal = self.CalcValue(board, f'{gene[0]}{gene[1]}')

                sumary += nodeVal * weight

            n += 1

        return 0 if n == 0 else sumary / n

if __name__ == "__main__":
    chromosomeTxt = '15081091 14171365 04161117 15051374 06071132 06120704 17060150 12050151 16041425 06120502 06130370 18000693 11060571 07170627 10170425 05160365 18080718 10121518 12031355 16010438 00040004 10111568 06121019 07131703 06020004 08051053 15160371 16050440 16020239 11081112 13040511 04140506'

    agent = Agent(chromosomeTxt, 1)

    board = [
        ['1', '_', '_'], 
        ['0', '0', '1'], 
        ['1', '0', '0']
        ]

    print(agent.FindBestMove(board))