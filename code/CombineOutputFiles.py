import os, sys, glob
from utilities import *

inFilePattern = sys.argv[1]
metric = sys.argv[2]
outFilePath = sys.argv[3]

outData = []

for inFilePath in glob.glob(inFilePattern):
    fileName = os.path.basename(inFilePath)
    fileItems = [line.rstrip().split("\t") for line in file(inFilePath)]

    if len(fileItems[0]) > 1:
        fileItems[0].append("Average AUC")
        fileItems[1].append(calculateMean([float(x) for x in fileItems[1]]))

    if len(outData) == 0:
        fileItems[0][-1] = fileItems[0][-1].replace("AUC", metric)
        outData.append(["Gene Set"] + fileItems[0])

    outData.append([fileName] + fileItems[1])

writeMatrixToFile(outData, outFilePath)
