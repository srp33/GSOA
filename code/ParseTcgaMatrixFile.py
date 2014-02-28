import os, sys, glob
from utilities import *

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

inHeaderItems = inFile.readline().rstrip().split("\t")
inHeaderItems = [inHeaderItems[0]] + [x[:16] for x in inHeaderItems[1:]]

outFile.write("\t".join(inHeaderItems) + "\n")

lineCount = 0
for line in inFile:
    lineItems = line.rstrip().split("\t")
    lineItems[0] = lineItems[0].split("|")[0]

    if lineItems[0] == "?":
        continue

    lineCount += 1
    if lineCount % 1000 == 0:
        print lineCount

    outFile.write("\t".join(lineItems) + "\n")

print lineCount

inFile.close()
outFile.close()
