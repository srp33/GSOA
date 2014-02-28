import os, sys, glob
from utilities import *

inFilePattern = sys.argv[1]
outFilePath = sys.argv[2]

def readFileLineItems(theFile, theFilePath):
    line = theFile.readline()

    if line == "":
        print "%s does not contain enough usable data." % theFilePath
        return None

    return line.rstrip().split("\t")

dataDict = {}

inFilePaths = glob.glob(inFilePattern)

print "Getting all sample IDs"
badFilePaths = []
filePathsNeedingHeaderAdjustment = []
for inFilePath in inFilePaths:
    inFile = open(inFilePath)
    headerItems = readFileLineItems(inFile, inFilePath)
    firstRowItems = readFileLineItems(inFile, inFilePath)
    inFile.close()

    # Make sure the file is valid
    if headerItems == None or firstRowItems == None:
        badFilePaths.append(inFilePath)
        continue

    # See if there is a header item for the row names. If so, remove it.
    if len(headerItems) == len(firstRowItems):
        del headerItems[0]
        filePathsNeedingHeaderAdjustment.append(inFilePath)

for badFilePath in badFilePaths:
    del inFilePaths[inFilePaths.index(badFilePath)]

# Identify unique features
uniqueFeatures = set()
for inFilePath in inFilePaths:
    print "Identifying unique features in %s" % inFilePath

    inFile = open(inFilePath)
    inFile.readline() # ignore header line
    for line in inFile:
        uniqueFeatures.add(line.split("\t")[0])
    inFile.close()

uniqueFeatures = sorted(list(uniqueFeatures))

outFile = open(outFilePath, 'w')
outFile.write("\t".join([""] + uniqueFeatures) + "\n")

for inFilePath in inFilePaths:
    print "Parsing data from %s" % inFilePath

    # Identify samples in this file
    inFile = open(inFilePath)
    sampleIDs = readFileLineItems(inFile, inFilePath)
    if inFilePath in filePathsNeedingHeaderAdjustment:
        del sampleIDs[0]
    inFile.close()

    for i in range(len(sampleIDs)):
        inFile = open(inFilePath)
        inFile.readline() # ignore header line

        sampleDict = {}
        for line in inFile:
            lineItems = line.rstrip().split("\t")
            feature = lineItems[0]
            value = lineItems[i + 1]
            sampleDict[feature] = value

        inFile.close()

        outRow = [sampleIDs[i]]
        for feature in uniqueFeatures:
            value = "?"
            if feature in sampleDict:
                value = sampleDict[feature]
            outRow.append(value)

        outFile.write("\t".join(outRow) + "\n")

outFile.close()
