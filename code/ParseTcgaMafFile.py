import os, sys, glob
from utilities import *

inFilePath = sys.argv[1]
excludeSilent = sys.argv[2] == "True"
outFilePath = sys.argv[3]

inFile = open(inFilePath)

inFileHeaderItems = inFile.readline().rstrip().split("\t")
sampleIndex = inFileHeaderItems.index("Tumor_Sample_Barcode")
geneIndex = inFileHeaderItems.index("Hugo_Symbol")
varClassificationIndex = inFileHeaderItems.index("Variant_Classification")

dataDict = {}
uniqueGenes = set()

inLineCount = 0
for line in inFile:
    inLineCount += 1
    if inLineCount % 10000 == 0:
        print "Read %i lines from %s" % (inLineCount, inFilePath)

    lineItems = line.rstrip().split("\t")
    sample = lineItems[sampleIndex][:16]
    gene = lineItems[geneIndex]
    varClassification = lineItems[varClassificationIndex]

    if excludeSilent and varClassification == "Silent":
        continue

    if sample not in dataDict:
        dataDict[sample] = set()

    dataDict[sample].add(gene)
    uniqueGenes.add(gene)

inFile.close()

uniqueSamples = sorted(dataDict.keys())
uniqueGenes = sorted(list(uniqueGenes))

outFile = open(outFilePath, 'w')
outFile.write("\t".join([""] + uniqueSamples) + "\n")
outGeneCount = 0
for gene in uniqueGenes:
    outGeneCount += 1
    if outGeneCount % 1000 == 0:
       print "Saved %i genes to %s" % (outGeneCount, outFilePath)

    outFile.write("\t".join([gene] + [("0", "1")[gene in dataDict[sample]] for sample in uniqueSamples]) + "\n")
outFile.close()
