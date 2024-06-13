import random as rnd
import os
import math

weightDigit = 3
processSize = 10
processDigit = lambda : max(math.ceil(math.log10(processSize)), 2)

populationSize = 32
crossoverRate = .3
selectionRate = .1
chromosomeSize = 100
mutationRate = 0.05

newFile = False

def RandomGeneParams():
    sourceType = rnd.randint(0, int((processSize != 0)))
    sourceID = rnd.randint(0, (18 if sourceType == 0 else processSize) - 1)

    sinkType = rnd.randint(0, int((processSize != 0)))
    sinkID = rnd.randint(0, (18 if sinkType == 0 else processSize) - 1)

    while CheckGeneParam((sourceType, sourceID, sinkType, sinkID)):
        sinkType = rnd.randint(0, 1)
        sinkID = rnd.randint(0, (18 if sinkType == 0 else processSize) - 1)

    weightSign = rnd.randint(0, 1)
    weightSize = rnd.randint(1, pow(10, weightDigit) - 1)

    return sourceType, sourceID, sinkType, sinkID, weightSign, weightSize

def CheckGeneParam(gene): return (gene[0] == 1) and (gene[2] == 1) and (gene[1] <= gene[3])

def EncryptGene(*args):
    args = args[0]
    gene = f'{args[0]}' + f'{{:0{processDigit()}d}}'.format(args[1])
    gene += f'{args[2]}' + f'{{:0{processDigit()}d}}'.format(args[3])
    gene += f'{args[4]}' + f'{{:0{weightDigit}d}}'.format(args[5])
    
    return gene

def DecryptGene(gene : str):
    gene = list(gene)

    data = []

    data += [gene.pop(0)] #source type

    data += [''.join(gene.pop(0) for i in range(processDigit()))] #source id

    data += [gene.pop(0)] #sink type
    
    data += [''.join(gene.pop(0) for i in range(processDigit()))] #sink id

    data += [gene.pop(0)] #weight sign

    data += [''.join(gene)] #weight size
    
    return list(map(int, data))

def ChromoCaller(path, number):
    with open(path, 'r') as f:
        chromosomes = [l.strip('\n\r ') for l in f.readlines()]

    return chromosomes[number if number <= len(chromosomes) else len(chromosomes)]

if __name__ == "__main__":
    #create file
    index = 0
    path = os.path.dirname(__file__) + "\\Gnomes\\ID-"

    while newFile:
        if not os.path.exists(path + str(index) + ".txt"):
            break
        index += 1

    if newFile:
        path += str(index) + ".txt"
    else:
        path += "4919.txt"

    f = open(path, 'w')

    #print file
    for i in range(populationSize):
        chromosome = ""
        for i in range(chromosomeSize):
            values = RandomGeneParams()

            chromosome += EncryptGene(values) + " "

        f.write(chromosome + "\n")
        
    f.close()