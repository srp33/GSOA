import os, sys, glob
import utilities

inFilePath = sys.argv[1]
numRows = int(sys.argv[2])
numCols = int(sys.argv[3])
outFilePath = sys.argv[4]

data = utilities.readMatrixFromFile(inFilePath, numRows)
outData = []

for row in data:
    if numCols > 0:
        row = row[:numCols]

    outData.append(row)

if outFilePath == "stdout":
    for row in outData:
        print row
else:
    utilities.writeMatrixToFile(outData, outFilePath)
