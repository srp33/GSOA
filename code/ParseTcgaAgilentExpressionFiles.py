import os, sys, glob

inFilePattern = sys.argv[1]
outFilePath = sys.argv[2]

dataDict = {}
overlappingGenes = set()

for inFilePath in sorted(glob.glob(inFilePattern)):
    print "Reading data from %s" % inFilePath
    inFile = open(inFilePath)
    sampleID = inFile.readline().rstrip().split("\t")[1][:16]
    inFile.readline() # Remove second header line

    thisFileDataDict = {}
    for line in inFile:
        lineItems = line.rstrip().split("\t")
        thisFileDataDict[lineItems[0]] = lineItems[1]
    inFile.close()

    if len(overlappingGenes) == 0:
        overlappingGenes = set(thisFileDataDict.keys())
    else:
        overlappingGenes = overlappingGenes & set(thisFileDataDict.keys())

    dataDict[sampleID] = thisFileDataDict

outFile = open(outFilePath, 'w')
outFile.write("\t".join([""] + dataDict.keys()) + "\n")
for gene in sorted(list(overlappingGenes)):
    print "Writing data to %s for %s" % (outFilePath, gene)
    outFile.write("\t".join([gene] + [dataDict[sampleID][gene] for sampleID in dataDict.keys()]) + "\n")
outFile.close()
