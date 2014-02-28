import os, sys, glob

dataFilePath = sys.argv[1]
classFilePath = sys.argv[2]
classificationAlgorithm = sys.argv[3]
numIterations = sys.argv[4]
outFilePath = sys.argv[5]

outText = "DATA_PROCESSORS=mlflex.dataprocessors.DelimitedDataProcessor(\"%s\");mlflex.dataprocessors.DelimitedDataProcessor(\"%s\")\n" % (dataFilePath, classFilePath)
outText += "CLASSIFICATION_ALGORITHMS=%s\n" % classificationAlgorithm
outText += "NUM_OUTER_CROSS_VALIDATION_FOLDS=1\n"
outText += "NUM_ITERATIONS=%s\n" % numIterations

outFile = open(outFilePath, 'w')
outFile.write(outText)
outFile.close()
