import os, sys, glob
from utilities import *

filePath = sys.argv[1]
outDirPath = sys.argv[2]

print "Formatting %s" % filePath

data = readMatrixFromFile(filePath)

data[0][0] = ""
data[0][1] = data[0][1][:16]
del data[1]

writeMatrixToFile(data, "%s/%s.txt" % (outDirPath, os.path.basename(filePath)))
