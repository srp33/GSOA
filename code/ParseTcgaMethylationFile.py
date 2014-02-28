import os, sys, glob
from utilities import *

dataFilePath = sys.argv[1]
adfFilePath = sys.argv[2]
outFilePath = sys.argv[3]

probeGeneDict = {}

adfFile = open(adfFilePath)
adfFile.readline()
for line in adfFile:
    lineItems = line.rstrip().split("\t")
    probeGeneDict[lineItems[0]] = lineItems[1]
adfFile.close()

dataFile = open(dataFilePath)
outFile = open(outFilePath, 'w')

headerItems = dataFile.readline().rstrip().split("\t")
headerItems = headerItems[:1] + [x[:16] for x in headerItems[1:]]
outFile.write("\t".join(headerItems) + "\n")

for line in dataFile:
    lineItems = line.rstrip().split("\t")
    lineItems[0] = probeGeneDict[lineItems[0]]
    outFile.write("\t".join(lineItems) + "\n")

outFile.close()
dataFile.close()
