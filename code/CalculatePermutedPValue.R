inFilePath = commandArgs()[7]
targetClass = commandArgs()[8]
numPermutations = as.integer(commandArgs()[9])
outPermutedAucsFilePath = commandArgs()[10]
outEmpiricalFilePath = commandArgs()[11]

suppressPackageStartupMessages(library(ROCR))

calcAuc = function(actual, prob)
{
  classes = unique(actual)

  pred = prediction(prob, actual)
  perf = performance(pred, measure="auc", x.measure="cutoff") 
  auc = as.numeric(deparse(as.numeric(perf@y.values)))

  return(auc)
}

data = read.table(inFilePath, sep="\t", stringsAsFactors=FALSE, header=TRUE, row.names=1, check.names=FALSE)

actualClasses = as.integer(data[,1]==targetClass)
actualProbabilities = as.numeric(data[,3])
actualAuc = calcAuc(actualClasses, actualProbabilities)

permutedAucs = NULL

for (i in 1:numPermutations)
{
  set.seed(i)
  permutedProbabilities = sample(actualProbabilities, length(actualProbabilities))
  permutedAucs = c(permutedAucs, calcAuc(actualClasses, permutedProbabilities))
}

write.table(permutedAucs, outPermutedAucsFilePath, col.names=FALSE, row.names=FALSE, quote=FALSE)

empiricalP = sum(permutedAucs >= actualAuc) / numPermutations
empiricalP = empiricalP + 1 / numPermutations
if (empiricalP > 1)
  empiricalP = 1

write.table(empiricalP, outEmpiricalFilePath, col.names=FALSE, row.names=FALSE, quote=FALSE)
print(actualAuc)
print(max(permutedAucs))
print(empiricalP)
