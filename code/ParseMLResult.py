import os, sys, glob

resultFilePath = sys.argv[1]
metric = sys.argv[2]
outFilePath = sys.argv[3]

for line in file(resultFilePath):
    lineItems = line.rstrip().split("\t")
    if metric == lineItems[0]:
        outFile = open(outFilePath, 'w')
        outFile.write(lineItems[1])
        outFile.close()
        break
