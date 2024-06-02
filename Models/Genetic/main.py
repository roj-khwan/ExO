import workshop

def Evaluate(board, chromosome):
    for i in range(9):
        print([gene for gene in chromosome if gene[3] == i and gene[2] == 0])
        pass

if __name__ == "__main__":
    chromosomeTxt = '02031479 05100187 08040203 06060281 12111431 11080178 11021488 12111672 12060062 10001396 10040713 12110350 08041131 06001097 10030216 02120054'

    chromosomeTxt = chromosomeTxt.split(' ')
    chromosome = list(map(workshop.DecryptGene, chromosomeTxt))

    Evaluate(None, chromosome)

    