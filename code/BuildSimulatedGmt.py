import os, sys, glob

outFilePath = "Simulated/genesets.gmt"

def writeLine(name, signalRange, randomRange):
    outItems = [name, name] + ["Gene%i" % i for i in signalRange] + ["Gene%i" % i for i in randomRange]
    outFile.write("\t".join(outItems) + "\n")

outFile = open(outFilePath, 'w')
writeLine("Signal1", range(991, 992), [])
writeLine("Signal2", range(991, 993), [])
writeLine("Signal10", range(991, 1001), [])
writeLine("Random1", [], range(1, 2))
writeLine("Random2", [], range(1, 3))
writeLine("Random10", [], range(1, 11))
writeLine("Random50", [], range(1, 51))
writeLine("Random100", [], range(1, 101))
writeLine("Random990", [], range(1, 991))
writeLine("Mixed2", range(991, 992), range(1, 2))
writeLine("Mixed10", range(991, 996), range(1, 6))
writeLine("Mixed50", range(991, 996), range(1, 46))
writeLine("Mixed100", range(991, 996), range(1, 96))
writeLine("Mixed990", range(991, 996), range(1, 986))
outFile.close()
