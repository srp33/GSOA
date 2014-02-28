import os, sys, glob
import utilities

gmtFilePath = sys.argv[1]
outFilePattern = sys.argv[2]

for line in file(gmtFilePath):
    lineItems = line.rstrip().split("\t")
    name = lineItems[0]
    genes = lineItems[2:]

    outFilePath = outFilePattern.replace("{PATHWAY_NAME}", name)
    utilities.writeVectorToFile(genes, outFilePath)
