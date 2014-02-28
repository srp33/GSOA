import os, sys, glob
import utilities

inFilePath = sys.argv[1]
filterValuesFilePathOrValue = sys.argv[2]
numHeaderRows = int(sys.argv[3])
outFilePath = sys.argv[4]

if os.path.exists(filterValuesFilePathOrValue):
    filterValues = set([x.strip() for x in file(filterValuesFilePathOrValue)])
else:
    filterValues = set(filterValuesFilePathOrValue.split(","))
    if len(filterValues) == 1:
        print "Warning: No file %s exists." % filterValues[0]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

for i in range(numHeaderRows):
    outFile.write(inFile.readline())

lineCount = 0
outLines = []
for line in inFile:
    lineCount += 1
    rowName = line[:line.index("\t")]

    if rowName in filterValues:
        outFile.write(line)

    if lineCount % 1000 == 0:
        print lineCount

print lineCount

inFile.close()
outFile.close()
