import glob, os, posix, sys, math, collections, json, difflib
from operator import itemgetter, attrgetter
import itertools
from random import uniform, sample
from collections import defaultdict
from scipy.stats import *

def readScalarFromFile(filePath):
    return readMatrixFromFile(filePath)[0][0]

def writeScalarToFile(x, filePath):
    outFile = open(filePath, 'w')
    outFile.write(x)
    outFile.close()

def readVectorFromFile(filePath):
    return [line.rstrip() for line in file(filePath)]

def writeVectorToFile(data, filePath):
    outFile = open(filePath, 'w')
    for x in data:
        outFile.write(str(x) + "\n")
    outFile.close()

def readMatrixFromFile(filePath, numLines=None):
    matrix = []
    for line in file(filePath):
        if numLines != None and len(matrix) >= numLines:
            break

        matrix.append(line.rstrip().split("\t"))

        if len(matrix) % 100000 == 0:
            print len(matrix)

    return matrix

def writeMatrixToFile(x, filePath, writeMode='w'):
    outFile = open(filePath, writeMode)
    writeMatrixToOpenFile(x, outFile)
    outFile.close()

def writeMatrixToOpenFile(x, outFile):
    for y in x:
        outFile.write("\t".join([str(z) for z in y]) + "\n")

def appendMatrixToFile(x, filePath):
    writeMatrixToFile(x, filePath, writeMode='a')

def readTextFromFile(filePath):
    text = ""

    for line in file(filePath):
        text += line

    return text

def calculateMean(values):
    if len(values) == 0:
        return float('nan')

    return sum(values) / len(values)

def calculateStandardDeviation(values):
    xbar = calculateMean(values)
    residuals = [x - xbar for x in values]
    residualsSquared = [x**2 for x in residuals]
    return math.sqrt(sum(residualsSquared) / (len(values) - 1))

def sortMatrix(data, columnIndex, reverse=False):
    data.sort(key=itemgetter(columnIndex), reverse=reverse)
    return data

def findNumGeneBins(numGenesSet):
    binOptions = [0, 1, 5, 10, 25, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 1000000]
    bins = []

    for i in range(len(binOptions))[1:]:
        if len([x for x in numGenesSet if x > binOptions[i-1] and x <= binOptions[i]]) > 0:
            bins.append(binOptions[i])

    if binOptions[-1] in bins:
        bins[-1] = max(list(numGenesSet))

    return bins

def getBin(numGenes, maxNumGenes):
    binOptions = [0, 1, 5, 10, 25, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 1000000]

    for i in range(len(binOptions))[1:]:
        if numGenes > binOptions[i-1] and numGenes <= binOptions[i]:
            if i == (len(binOptions) - 1):
                return maxNumGenes
            return binOptions[i]

def getConfigValue(configFilePath, key):
    configDict = {}
    for line in file(configFilePath):
        if line.startswith("#"):
            continue

        lineItems = line.rstrip().split("=")
        if lineItems[0] == key:
            return lineItems[1]

    print "No %s key was found." % key
    return None

def calculateSpearmanCoefficient(xList, yList):
    return stats.spearmanr(xList, yList)[0]
