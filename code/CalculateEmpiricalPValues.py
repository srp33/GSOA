import os, sys, glob, random, math
from utilities import *

dataDirPath = sys.argv[1]
resultDirPath = sys.argv[2]
randomResultDirPath = sys.argv[3]
outDirPath = sys.argv[4]

dataFileNumGenesDict = {}
for dataFilePath in glob.glob(dataDirPath + "/*"):
    numGenes = len([line for line in file(dataFilePath)]) - 1
    dataFileNumGenesDict[dataFilePath] = numGenes
maxNumGenes = max(dataFileNumGenesDict.values())

for dataFilePath in glob.glob(dataDirPath + "/*"):
    geneSet = os.path.basename(dataFilePath)
    numGenes = dataFileNumGenesDict[dataFilePath]

    actualResultLines = [line.rstrip().split("\t") for line in file(resultDirPath + "/" + geneSet)]
    actualResultHeaderItems = actualResultLines.pop(0)
    actualResult = [float(x) for x in actualResultLines[0]]

    randomResults = []
    for randomFilePath in glob.glob(randomResultDirPath + "/%iGenes___*" % getBin(numGenes, maxNumGenes)):
        randomResultLine = [line.rstrip().split("\t") for line in file(randomFilePath)][1]
        randomResult = [float(x) for x in randomResultLine]
        randomResults.append(randomResult)

    empiricalResults = []
    for i in range(len(actualResult)):
        actualValue = actualResult[i]
        randomValues = [x[i] for x in randomResults]

        numRandomGreaterThanActual = float(len([x for x in randomValues if x >= actualValue]))
        numDecimalPlaces = int(math.log10(float(len(randomValues))))
        empiricalPValue = numRandomGreaterThanActual / float(len(randomValues))
        empiricalPValueText = ("%." + str(numDecimalPlaces) + "f") % empiricalPValue

        empiricalResults.append(empiricalPValueText)

    outFilePath = outDirPath + "/" + geneSet
    outFile = open(outFilePath, 'w')
    outFile.write("\t".join(actualResultHeaderItems) + "\n")
    outFile.write("\t".join(empiricalResults) + "\n")
    outFile.close()
