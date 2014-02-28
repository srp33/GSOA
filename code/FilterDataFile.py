import os, sys, glob
from utilities import *

inFilePath = sys.argv[1]
filterFilePath = sys.argv[2]
outFilePath = sys.argv[3]

filterValues = set(readVectorFromFile(filterFilePath))

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

# Print header line
outFile.write(inFile.readline())

outText = ""
count = 0
for line in inFile:
    count += 1
    if count % 1000 == 0:
        print count
    value = line.split("\t")[0]
    if value in filterValues:
        outFile.write(line)

inFile.close()
outFile.close()
