import os, sys, glob

inFilePath = sys.argv[1]
threshold = float(sys.argv[2])
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

outFile.write(inFile.readline())
for line in inFile:
    lineItems = line.rstrip().split("\t")
    outFile.write("\t".join(lineItems[:1] + [("0", "1")[float(x) >= threshold] for x in lineItems[1:]]) + "\n")

inFile.close()
outFile.close()
