import os, sys, glob

gmtFilePath = sys.argv[1]

for line in file(gmtFilePath):
    lineItems = line.rstrip().split("\t")
    print lineItems[0]
