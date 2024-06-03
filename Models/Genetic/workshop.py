import random as rnd
import os

weightDigit = 3
processSize = 10

populationSize = 10
chromosomeSize = 32

newFile = True

def RandomGeneParams():
    sourceType = rnd.randint(0, int((processSize != 0)))
    sourceID = rnd.randint(0, (9 if sourceType == 0 else processSize) - 1)

    sinkType = rnd.randint(0, int((processSize != 0)))
    sinkID = rnd.randint(0, (9 if sinkType == 0 else processSize) - 1)

    while (sourceType == 1) and (sinkType == 1) and (sourceID >= sinkID):
        sinkType = rnd.randint(0, 1)
        sinkID = rnd.randint(0, (9 if sinkType == 0 else processSize) - 1)

    weightSign = rnd.randint(0, 1)
    weightSize = rnd.randint(1, pow(9, weightDigit))

    return sourceType, sourceID, sinkType, sinkID, weightSign, weightSize

def EncryptGene(*args):
    args = args[0]
    gene = f'{args[0]}{args[1]}'
    gene += f'{args[2]}{args[3]}'
    gene += f'{args[4]}{"{:03d}".format(args[5])}'
    
    return gene

def DecryptGene(gene):
    data = []
    data.append(int(gene[0])) #source type
    data.append(int(gene[1])) #source id
    data.append(int(gene[2])) #sink type
    data.append(int(gene[3])) #source id
    data.append(int(gene[4])) #weight sign
    data.append(int(gene[5:])) #weight size
    
    return data

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
        path = "chromosomes\\ID-4919.txt"

    f = open(path, 'w')

    #print file
    for i in range(populationSize):
        chromosome = ""
        for i in range(chromosomeSize):
            values = RandomGeneParams()

            chromosome += EncryptGene(values) + " "

        f.write(chromosome + "\n")
        
    f.close()