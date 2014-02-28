import os, sys, glob
from utilities import *

inFilePath1 = sys.argv[1]
inFilePath2 = sys.argv[2]
numValues = int(sys.argv[3])

print "Identifying overlapping samples"
inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)

samples1 = inFile1.readline().rstrip().split("\t")[1:]
samples2 = inFile2.readline().rstrip().split("\t")[1:]
overlappingSamples = set(samples1) & set(samples2)

sampleIndices1 = [(samples1.index(sample) + 1) for sample in overlappingSamples]
sampleIndices2 = [(samples2.index(sample) + 1) for sample in overlappingSamples]

print "Identifying overlapping genes"
genes1 = [x.rstrip().split("\t")[0] for x in inFile1 if "null" not in x]
genes2 = [x.rstrip().split("\t")[0] for x in inFile2 if "null" not in x]
overlappingGenes = list(set(genes1) & set(genes2))[:numValues]

inFile2.close()
inFile1.close()

inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)
inFile1.readline()
inFile2.readline()

dataDict1 = {}
dataDict2 = {}

print "Parsing through %s" % inFilePath1
for line in inFile1:
    lineItems = line.rstrip().split("\t")

    if lineItems[0] in overlappingGenes:
        dataDict1[lineItems[0]] = [float(lineItems[i]) for i in sampleIndices1]

print "Parsing through %s" % inFilePath2
for line in inFile2:
    lineItems = line.rstrip().split("\t")

    if lineItems[0] in overlappingGenes:
        dataDict2[lineItems[0]] = [float(lineItems[i]) for i in sampleIndices2]


print "Calculating correlations"
corrs = []
for gene in overlappingGenes:
    corr = calculateSpearmanCoefficient(dataDict1[gene], dataDict2[gene])
    if str(corr) == 'nan':
        continue

    corrs.append(corr)

inFile2.close()
inFile1.close()

print "Minimum Spearman's rho for %i genes: %.6f" % (numValues, min(corrs))
print "Average Spearman's rho for %i genes: %.6f" % (numValues, calculateMean(corrs))
print "Maximum Spearman's rho for %i genes: %.6f" % (numValues, max(corrs))
