import os, sys, glob
from utilities import *

inFilePattern = sys.argv[1]
outFilePath = sys.argv[2]

outItems = []
for inFilePath in glob.glob(inFilePattern):
    cancerType = os.path.basename(inFilePath).replace("tcga_", "").replace("_whitelist", "")
    for line in file(inFilePath):
        sample = line.rstrip()[:16]
        outItems.append([sample, cancerType])

writeMatrixToFile(outItems, outFilePath)
