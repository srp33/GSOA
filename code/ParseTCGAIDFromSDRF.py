import os, sys, glob
from utilities import *

dataFileName = sys.argv[1]
metaFileName = sys.argv[2]

meta = readMatrixFromFile(metaFileName)

headerItems = meta.pop(0)

id = [x for x in meta if x[headerItems.index("Derived Data File")] == dataFileName][0][1]

print id[:16]
