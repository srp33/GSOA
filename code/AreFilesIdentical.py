import os, sys, glob

inFilePath1 = sys.argv[1]
inFilePath2 = sys.argv[2]

inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)

areIdentical = True

for line1 in inFile1:
    line2 = inFile2.readline()
    if line1 != line2:
        areIdentical = False
        break

inFile2.close()
inFile1.close()

print areIdentical
