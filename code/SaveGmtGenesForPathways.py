import os, sys, glob

gmtFilePath = sys.argv[1]
outDirPath = sys.argv[2]

for line in file(gmtFilePath):
    lineItems = line.rstrip().split("\t")

    outFile = open(outDirPath + "/" + lineItems[0], 'w')
    outFile.write("\n".join(lineItems[2:]) + "\n")
    outFile.close()
