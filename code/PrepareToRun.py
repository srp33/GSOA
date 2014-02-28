import os, sys, glob, random
from utilities import *

gmtFilePattern = sys.argv[1]
classesFilePath = sys.argv[2]
inDataFilePath = sys.argv[3]
numRandomIterations = int(sys.argv[4])
outMainDataDirPath = sys.argv[5]
outMainResultDirPath = sys.argv[6]
outRandomDataDirPath = sys.argv[7]
outRandomResultDirPath = sys.argv[8]
commandPrefix = sys.argv[9]
outCommandFilePath = sys.argv[10]
configFilePath = sys.argv[11]

def saveGeneSetData(geneSet, description, geneSetData, outDataDirPath, outResultDirPath):
    if len(geneSetData) == 0:
        print "No data to save for %s, %s" % (description, geneSet)
        return

    outputText = ""
    for item in geneSetData:
        outputText += "\t".join([str(x) for x in item]) + "\n"
    outputText += "\t".join([classDict[sample] for sample in samples]) + "\n"

    print "Saving data for %s, %s" % (description, geneSet)
    outFilePath = outDataDirPath + "/" + geneSet
    outFile = open(outFilePath, 'w')
    outFile.write(outputText)
    outFile.close()

    commands.append("%s %s %s %s/%s %s" % (commandPrefix, description, outFilePath, outResultDirPath, geneSet, configFilePath))

geneSetDict = {}
geneSetUniqueGenes = set()

for gmtFilePath in glob.glob(gmtFilePattern):
    for line in file(gmtFilePath):
        lineItems = line.rstrip().split("\t")
        geneSet = lineItems[0]
        genes = lineItems[2:]

        geneSetDict[geneSet] = genes
        geneSetUniqueGenes.update(genes)

if len(geneSetDict) == 0:
    print "No gene sets could be found."
    exit(1)

allClassDict = {}

for line in file(classesFilePath):
    lineItems = line.rstrip().split("\t")
    sampleID = lineItems[0]
    sampleClass = lineItems[1]
    allClassDict[sampleID] = sampleClass

if len(allClassDict) == 0:
    print "No class information could be found."
    exit(1)

inDataFile = open(inDataFilePath)

samples = inDataFile.readline().rstrip().split("\t")
samples.pop(0) # Remove first column header
uniqueDataSamples = set(samples)

classDict = {}
for sample in samples:
    if sample in allClassDict:
        classDict[sample] = allClassDict[sample]

# Count the number of samples in each class
classSampleCountDict = {}
for sample in samples:
    if sample in classDict:
        classSampleCountDict[classDict[sample]] = classSampleCountDict.setdefault(classDict[sample], 0) + 1

# Remove any class that does not have an adequate number of samples
n_folds = int(getConfigValue(configFilePath, "n_folds"))
for sampleClass in classSampleCountDict:
    if classSampleCountDict[sampleClass] < n_folds:
        print "Removing %i samples of class %s because there are not enough samples to perform cross validation." % (classSampleCountDict[sampleClass], sampleClass)
        for sample in classDict.keys():
            if classDict[sample] == sampleClass:
                del classDict[sample]

sampleIndices = [i for i in range(len(samples)) if samples[i] in classDict.keys()]
samples = [x for x in samples if x in classDict.keys()] # keeps order of samples

if len(samples) == 0:
    print "No samples (columns) in the data file contained class information."
    exit(1)
else:
    print "%i samples (columns) in the data file contained class information." % len(sampleIndices)

# Build a dict that contains data for each gene
numDataRows = 0
numDataRowsInGeneSets = 0
dataDict = {}
for line in inDataFile:
    lineItems = line.rstrip().split("\t")
    gene = lineItems.pop(0)
    values = [lineItems[i] for i in sampleIndices]

    if len(set(["null", "nan"]) & set(values)) > 0:
        continue

    if gene in geneSetUniqueGenes:
        numDataRowsInGeneSets += 1
    numDataRows += 1

    if gene not in dataDict:
        dataDict[gene] = []
    dataDict[gene].append(values) # Genes with multiple rows will have multiple entries

inDataFile.close()

# Select only genes for which there are data
for geneSet in geneSetDict.keys():
    geneSetDict[geneSet] = list(set(geneSetDict[geneSet]) & set(dataDict.keys()))

commands = []

# Save data for each gene set
geneSetLengths = set()
for geneSet in sorted(geneSetDict.keys()):
    geneSetData = []

    for gene in geneSetDict[geneSet]:
        if gene in dataDict.keys():
            for values in dataDict[gene]:
                geneSetData.append(values)

    saveGeneSetData(geneSet, "main", geneSetData, outMainDataDirPath, outMainResultDirPath)
    geneSetLengths.add(len(geneSetData))

bins = findNumGeneBins(geneSetLengths)

print "%i genes had data for all samples." % numDataRows
print "%i genes had data for all samples and belonged to at least one gene set." % numDataRowsInGeneSets
print "The following bins will be used for random selection: %s" % ", ".join([str(x) for x in bins])

# Create data list that will allow us to randomly pick data rows, even if genes have multiple values
dataList = []
for gene in dataDict.keys():
    for item in dataDict[gene]:
        dataList.append(item)
    del dataDict[gene] # To save memory

random.seed(1)
for numGenes in bins:
    for i in range(numRandomIterations):
        randomGeneSet = "%iGenes___%i" % (numGenes, i)

        randomDataIndices = range(len(dataList))
        random.shuffle(randomDataIndices)
        randomGeneSetData = [dataList[i] for i in randomDataIndices[:numGenes]]

        saveGeneSetData(randomGeneSet, "random", randomGeneSetData, outRandomDataDirPath, outRandomResultDirPath)

print "%i commands will be executed." % len(commands)

outCommandFile = open(outCommandFilePath, 'w')
outCommandFile.write("set -o errexit\n")
outCommandFile.write("\n".join(commands) + "\n")
outCommandFile.close()
