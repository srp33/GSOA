import os, sys, glob
from operator import itemgetter, attrgetter
import numpy
import scipy
import sklearn.svm
import sklearn.preprocessing
import sklearn.cross_validation
import sklearn.metrics
from utilities import *

description = sys.argv[1]
dataFilePath = sys.argv[2]
outFilePath = sys.argv[3]
configFilePath = sys.argv[4]

def predictForTarget(target):
    modTargets = numpy.array([(-1.0, 1.0)[x == target] for x in targets])

    mean_tpr = 0.0
    mean_fpr = numpy.linspace(0, 1, 100)

    for trainIndices, testIndices in cv:
        if algorithm.startswith("svm"):
            clf = sklearn.svm.SVC(C=1.0, kernel=algorithm.replace("svm", ""), gamma=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight='auto', verbose=False, max_iter=-1, random_state=0)

        trainData = data[trainIndices,]
        trainTargets = modTargets[trainIndices]
        testData = data[testIndices,]
        testTargets = modTargets[testIndices]

        model = clf.fit(trainData, trainTargets)
        probs = model.predict_proba(testData)[:,1]

        fpr, tpr, thresholds = sklearn.metrics.roc_curve(testTargets, probs)
        mean_tpr += scipy.interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = sklearn.metrics.auc(fpr, tpr)

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0

    return sklearn.metrics.auc(mean_fpr, mean_tpr)

algorithm = getConfigValue(configFilePath, "algorithm")
n_folds = int(getConfigValue(configFilePath, "n_folds"))

data = [[y for y in line.rstrip().split("\t")] for line in file(dataFilePath)]
targets = data.pop(-1)
data = [[float(y) for y in x] for x in data]
data = numpy.transpose(numpy.array(data))

data = sklearn.preprocessing.StandardScaler().fit_transform(data)
cv = sklearn.cross_validation.StratifiedKFold(numpy.array(targets), n_folds=n_folds, indices=True)

uniqueTargets = sorted(list(set(targets)))

outFile = open(outFilePath, 'w')

if len(uniqueTargets) == 2:
    outFile.write("AUC\n")
    outFile.write("%.8f\n" % predictForTarget(uniqueTargets[0]))
else:
    outFile.write("\t".join(uniqueTargets) + "\n")
    outFile.write("\t".join(["%.8f" % predictForTarget(target) for target in uniqueTargets]) + "\n")

outFile.close()

numTasks = len(glob.glob(os.path.dirname(dataFilePath) + "/*"))
numCompleted = len(glob.glob(os.path.dirname(outFilePath) + "/*"))
print "%i/%i gene sets complete (%s)" % (numCompleted, numTasks, description)
